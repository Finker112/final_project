import joblib
import mlflow.sklearn

# 1. 从 MLflow 运行记录中加载真实模型对象
RUN_ID = "3c0b0feca5ed4ff9848cfb72aa111689"
model = mlflow.sklearn.load_model(f"runs:/{RUN_ID}/model")

# 2. 保存为标准 joblib 单文件
joblib.dump(model, "ml/prod_model.joblib")

print("✅ 模型导出成功")
print("模型类型:", type(model))
print("测试预测:", model.predict([[2.5, 14, 2]]))