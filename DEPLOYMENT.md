# Kronos GitHub Actions 部署指南

## 概述

这个项目现在已经配置为可以在 GitHub Actions 中自动运行，每小时更新一次 BTC/USDT 预测数据并可选择部署到 Cloudflare Pages。

## 功能特性

✅ **完全支持 GitHub Actions**：Python 脚本可以在 Ubuntu 环境中正常运行  
✅ **自动依赖管理**：使用 pip cache 加速安装  
✅ **无头环境优化**：matplotlib 使用 Agg 后端  
✅ **智能 Git 处理**：CI 环境中由 Actions 处理，本地环境保持原有逻辑  
✅ **定时执行**：每小时第 5 分钟自动运行  
✅ **手动触发**：支持 workflow_dispatch  
✅ **可选 Cloudflare Pages 部署**

## 设置步骤

### 1. 推送代码到 GitHub

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### 2. 启用 GitHub Actions

1. 进入你的 GitHub 仓库
2. 点击 "Actions" 标签
3. 如果看到工作流，点击 "Enable workflow"

### 3. 测试运行

点击 "Actions" → "Update Kronos Predictions and Deploy" → "Run workflow" 手动触发一次测试。

### 4. （可选）配置 Cloudflare Pages 部署

如果你想自动部署到 Cloudflare Pages：

1. 获取 Cloudflare API Token：
   - 登录 Cloudflare Dashboard
   - 进入 "My Profile" → "API Tokens"
   - 创建自定义 Token，权限：`Zone:Zone:Read, Zone:Page Rule:Edit`

2. 获取 Account ID：
   - 在 Cloudflare Dashboard 右侧边栏可以找到

3. 在 GitHub 仓库设置 Secrets：
   - 进入仓库 "Settings" → "Secrets and variables" → "Actions"
   - 添加以下 secrets：
     - `CLOUDFLARE_API_TOKEN`: 你的 API Token
     - `CLOUDFLARE_ACCOUNT_ID`: 你的 Account ID

## 工作流说明

### 触发条件
- **定时执行**：每小时第 5 分钟（UTC 时间）
- **手动触发**：在 Actions 页面手动运行
- **代码推送**：推送到 main/master 分支时

### 执行步骤
1. 检出代码
2. 设置 Python 3.10 环境
3. 安装依赖（使用缓存加速）
4. 创建模型目录
5. 运行预测脚本
6. 提交并推送更新的文件
7. （可选）部署到 Cloudflare Pages

### 处理的文件
- `index.html` - 更新预测指标
- `prediction_chart_1h.png` - 1小时预测图表
- `prediction_chart_4h.png` - 4小时预测图表  
- `prediction_chart_1d.png` - 1天预测图表

## 本地开发

本地运行时，脚本会：
- 执行完整的 git 操作
- 启动调度器持续运行

CI 环境中，脚本会：
- 跳过 git 操作（由 Actions 处理）
- 只运行一次就退出

## 故障排除

### 常见问题

1. **模型下载失败**
   - 检查网络连接
   - HuggingFace 模型会自动下载到临时目录

2. **依赖安装超时**
   - torch 等包较大，首次运行可能需要几分钟
   - 后续运行会使用缓存

3. **Git 推送失败**
   - 确保仓库有写入权限
   - 检查是否有冲突的并发运行

### 查看日志

在 GitHub Actions 页面可以查看详细的运行日志，包括：
- Python 脚本输出
- 模型加载进度
- 预测生成过程
- Git 操作结果

## 成本考虑

- **GitHub Actions**：每月 2000 分钟免费额度
- **预估使用**：每次运行约 3-5 分钟，每月约 150 分钟
- **Cloudflare Pages**：免费版足够使用

## 监控

建议设置以下监控：
- GitHub Actions 运行状态通知
- 网站可用性监控
- 预测数据更新时间检查