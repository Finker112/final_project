from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_v1(n_samples=2000):
    """v1原始数据集：带异常值、缺失值，无衍生特征"""
    np.random.seed(42)
    distance = np.random.exponential(scale=2.5, size=n_samples)
    pickup_time = [datetime(2024, 1, 1) + timedelta(minutes=np.random.randint(0, 1440))
                   for _ in range(n_samples)]

    df = pd.DataFrame({
        "trip_distance": distance,
        "pickup_datetime": pickup_time
    })

    # 加入异常值
    df.loc[0:50, "trip_distance"] = 0
    df.loc[51:80, "trip_distance"] = 100
    # 加入缺失值
    df.loc[100:150, "trip_distance"] = np.nan

    # 目标变量：行程时长（秒）
    df["trip_duration"] = df["trip_distance"] * 120 + np.random.normal(0, 60, n_samples)
    df.loc[200:220, "trip_duration"] = 10000  # 异常时长
    return df


def generate_v2(df_v1):
    """v2清洗版本：过滤异常、填充缺失、新增时间特征"""
    df = df_v1.copy()
    # 过滤异常
    df = df[(df["trip_distance"] > 0) & (df["trip_distance"] < 30)]
    df = df[(df["trip_duration"] >= 60) & (df["trip_duration"] <= 3 * 3600)]
    # 填充缺失
    df["trip_distance"] = df["trip_distance"].fillna(df["trip_distance"].median())
    # 新增特征
    df["hour"] = df["pickup_datetime"].dt.hour
    df["weekday"] = df["pickup_datetime"].dt.weekday
    return df


if __name__ == "__main__":
    df_v1 = generate_v1()
    df_v1.to_csv("data/taxi_v1.csv", index=False)
    print(f"✅ v1生成完成，行数：{len(df_v1)}")

    df_v2 = generate_v2(df_v1)
    df_v2.to_csv("data/taxi_v2.csv", index=False)
    print(f"✅ v2生成完成，行数：{len(df_v2)}")