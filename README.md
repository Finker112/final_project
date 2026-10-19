# 出租车行程时间预测 MLOps项目
## 项目概述
基于机器学习的出租车行程时间预测服务，完整实现DevOps与MLOps工程化流程。

## 分支策略
- feature/*：功能开发分支
- dev：开发集成分支
- staging：预发布验证分支
- main：生产分支

合并路径：feature → dev → staging → main

## 流水线流程
代码提交 → PR到受保护分支 → CI执行（测试/代码检查/镜像构建）→ 合并到dev → 合并到staging（构建预发布镜像）→ 合并到main（构建生产镜像）

## 目录结构
├── app/                # 推理服务
├── ml/                 # 机器学习模块
│   ├── train.py        # 训练脚本（MLflow集成）
│   ├── data_pipeline.py # 数据处理
│   ├── configs/        # 配置文件
│   ├── README_data.md  # 数据集说明
│   ├── README_experiments.md # 实验说明
│   └── current_model.md # 当前生产模型
├── tests/              # 单元测试
├── data/               # 数据集（DVC管理）
├── .github/workflows/  # CI/CD流水线
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
└── DEPLOYMENT.md