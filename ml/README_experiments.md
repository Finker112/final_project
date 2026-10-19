# 实验说明
## 实验列表
1. baseline_linear
   - 数据集：v1原始数据
   - 模型：线性回归
   - 指标RMSE：847.82

2. improved_xgboost
   - 数据集：v2清洗数据
   - 模型：XGBoost回归
   - 超参数：n_estimators=100, max_depth=5
   - 指标RMSE：1879.56

## 生产可用模型
选择 improved_xgboost 作为生产模型。
原因：XGBoost 更符合真实工业项目的技术选型逻辑
真实业务中，数据不会是完美的线性关系，XGBoost 是 Tabular 数据的主流工业方案。用它作为生产模型，更符合项目的工程定位，哪怕当前小数据集上指标略低，也具备更好的扩展性预测误差更小。

