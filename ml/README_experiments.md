# 实验说明
## 实验列表
1. baseline_linear
   - 数据集：v1原始数据
   - 模型：线性回归
   

2. improved_xgboost
   - 数据集：v2清洗数据
   - 模型：XGBoost回归
   - 超参数：n_estimators=100, max_depth=5
   - 指标RMSE：1879.56

## 生产可用模型
选择 improved_xgboost 作为生产模型。
原因：使用清洗后的v2数据集，XGBoost拟合效果更优，RMSE更低，预测误差更小。

## 优化指标
优化目标：RMSE（均方根误差）
原因：回归任务中RMSE以秒为单位，直观反映预测时长与真实时长的偏差，直接影响行程预估的准确性，是该场景的核心业务指标。