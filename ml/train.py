import os
import subprocess
import numpy as np
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# ===================== 路径配置 =====================
# 自动获取项目根目录（脚本在 ml/ 下，上一级就是根目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取当前 Git commit SHA（内置命令实现，不依赖第三方库）
def get_git_sha():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"

git_sha = get_git_sha()

# 信任的模型类型（解决MLflow安全报错）
TRUSTED_TYPES = [
    "xgboost.sklearn.XGBRegressor",
    "xgboost.core.Booster"
]


# ===================== 实验函数 =====================
def run_experiment(dataset_path, model_name, model, params=None):
    # 拼接完整数据路径
    full_data_path = os.path.join(BASE_DIR, dataset_path)
    df = pd.read_csv(full_data_path)

    # 基础缺失值处理（线性回归不支持NaN，直接删除含缺失样本）
    df = df.dropna(subset=["trip_distance", "trip_duration"])

    # 自动适配特征列
    if "hour" in df.columns:
        features = ["trip_distance", "hour", "weekday"]
    else:
        features = ["trip_distance"]

    X = df[features]
    y = df["trip_duration"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 设置实验名称
    mlflow.set_experiment("taxi_trip_duration")

    with mlflow.start_run(run_name=model_name):
        # 1. 记录元数据
        mlflow.set_tag("git_commit_sha", git_sha)
        mlflow.log_param("dataset_path", dataset_path)
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("missing_value_strategy", "dropna")
        mlflow.log_param("feature_count", len(features))
        if params:
            mlflow.log_params(params)

        # 2. 模型训练
        model.fit(X_train, y_train)

        # 3. 评估并记录指标（兼容旧版sklearn，手动计算RMSE）
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mlflow.log_metric("rmse", round(rmse, 2))

        # 4. 保存模型工件（添加信任类型，解决安全报错）
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            skops_trusted_types=TRUSTED_TYPES
        )

        print(f"✅ 实验 {model_name} 完成 | RMSE: {rmse:.2f} | 特征数: {len(features)}")
        return rmse


# ===================== 主程序：运行两组实验 =====================
if __name__ == "__main__":
    # 实验1：基线模型 - 线性回归 + v1原始数据集
    run_experiment(
        dataset_path="data/taxi_v1.csv",
        model_name="baseline_linear",
        model=LinearRegression()
    )

    # 实验2：改进模型 - XGBoost + v2清洗数据集
    run_experiment(
        dataset_path="data/taxi_v2.csv",
        model_name="improved_xgboost",
        model=xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            random_state=42
        ),
        params={"n_estimators": 100, "max_depth": 5}
    )

    print("\n🎉 两组实验全部运行完成，可执行 mlflow ui 查看结果")