# 部署说明
## 流水线触发规则
1. PR提交到 dev / staging / main 分支：自动触发CI流水线
   - 执行代码静态检查
   - 运行单元测试
   - 构建Docker镜像
   - CI失败则禁止合并PR

2. 合并到 staging 分支：
   - 读取GitHub Secrets中staging环境变量，生成staging.env
   - 构建staging环境Docker镜像
   - 不执行实际线上部署

3. 合并到 main 分支：
   - 读取GitHub Secrets中production环境变量，生成prod.env
   - 构建生产环境Docker镜像
   - 不执行实际线上部署

## 环境变量
所有敏感配置通过GitHub Secrets管理，不提交到代码仓库。