# Kronos 自动更新系统使用指南

本指南将帮助你设置和使用Kronos预测数据的自动更新系统。

## 📋 系统要求

- Python 3.7+
- Git
- 已配置的GitHub仓库
- 网络连接

## 🚀 快速开始

### 1. 检查环境

确保以下工具已安装并可在命令行中使用：

```bash
# 检查Python
python --version

# 检查Git
git --version
```

### 2. 配置Git（如果尚未配置）

```bash
# 设置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 验证配置
git config --list
```

### 3. 运行自动更新

**方法一：使用批处理脚本（Windows推荐）**

双击 `run_update.bat` 文件，或在命令行中运行：

```cmd
run_update.bat
```

**方法二：直接运行Python脚本**

```bash
python auto_update.py
```

## 📁 文件说明

### 核心文件

- `auto_update.py` - 主要的自动更新脚本
- `run_update.bat` - Windows批处理脚本，方便运行
- `config.py` - 配置文件，可自定义各种设置
- `update.log` - 运行日志文件（自动生成）

### 脚本功能

1. **预测数据更新**：运行 `update_predictions.py` 生成最新预测
2. **Git状态检查**：检查是否有文件变更
3. **自动提交**：将变更提交到Git仓库
4. **推送到GitHub**：自动推送到远程仓库
5. **日志记录**：详细记录每次运行的情况

## ⚙️ 配置选项

编辑 `config.py` 文件来自定义设置：

### Git配置
```python
GIT_CONFIG = {
    'main_branch': 'main',  # 或 'master'
    'remote_name': 'origin',
    'commit_message_template': 'Auto update predictions - {timestamp}'
}
```

### 日志配置
```python
LOG_CONFIG = {
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'console_output': True,
    'max_log_size_mb': 10
}
```

### 预测配置
```python
PREDICTION_CONFIG = {
    'timeout_seconds': 300,
    'retry_count': 2,
    'retry_delay': 30
}
```

## 🕐 设置定时任务

### Windows任务计划程序

1. 按 `Win + R`，输入 `taskschd.msc`
2. 点击"创建基本任务"
3. 设置任务名称："Kronos预测更新"
4. 选择触发器："每天"或"每小时"
5. 设置操作：
   - 程序：`cmd`
   - 参数：`/c "C:\path\to\your\project\run_update.bat"`
   - 起始于：你的项目目录

### Linux/Mac Crontab

```bash
# 编辑crontab
crontab -e

# 每小时运行一次
0 * * * * cd /path/to/kronos-demo-master && python3 auto_update.py >> cron.log 2>&1

# 每4小时运行一次
0 */4 * * * cd /path/to/kronos-demo-master && python3 auto_update.py >> cron.log 2>&1
```

## 📊 监控和日志

### 查看日志

```bash
# 查看最新日志
tail -f update.log

# 查看完整日志
cat update.log
```

### 日志内容示例

```
2024-01-15 10:00:01,123 - INFO - === Kronos自动更新开始 (2024-01-15 10:00:01) ===
2024-01-15 10:00:01,124 - INFO - 工作目录: C:\Users\Zero\Kronos-demo-master
2024-01-15 10:00:01,125 - INFO - 检查运行环境...
2024-01-15 10:00:01,126 - INFO - Python版本: 3.9.7
2024-01-15 10:00:01,127 - INFO - Git版本: git version 2.33.0
2024-01-15 10:00:01,128 - INFO - 开始更新预测数据...
2024-01-15 10:00:15,456 - INFO - 预测数据更新成功
2024-01-15 10:00:15,457 - INFO - 检测到以下文件变更:
 M prediction_chart_1h.png
 M prediction_chart_4h.png
 M prediction_chart_1d.png
2024-01-15 10:00:15,458 - INFO - 开始推送更新到GitHub...
2024-01-15 10:00:16,789 - INFO - 成功推送到GitHub
2024-01-15 10:00:16,790 - INFO - === 自动更新结束 (2024-01-15 10:00:16) ===
2024-01-15 10:00:16,791 - INFO - 总耗时: 15.67秒
2024-01-15 10:00:16,792 - INFO - 状态: 成功
```

## 🔧 故障排除

### 常见问题

**1. Git推送失败**
```
错误: Git push失败: Permission denied
```
解决方案：
- 检查SSH密钥配置
- 或使用Personal Access Token
- 确保有仓库写入权限

**2. Python脚本执行失败**
```
错误: 未找到update_predictions.py文件
```
解决方案：
- 确保在正确的目录中运行
- 检查文件是否存在

**3. 网络连接问题**
```
错误: 无法连接到远程仓库
```
解决方案：
- 检查网络连接
- 验证GitHub访问权限
- 检查防火墙设置

### 调试模式

修改 `config.py` 中的日志级别：

```python
LOG_CONFIG = {
    'log_level': 'DEBUG',  # 显示详细调试信息
    # ...
}
```

## 📈 推荐运行频率

- **开发测试**：手动运行或每小时
- **生产环境**：每4小时或每天
- **高频更新**：每30分钟（注意API限制）

## 🔒 安全注意事项

1. **不要在代码中硬编码密码或密钥**
2. **使用SSH密钥或Personal Access Token进行Git认证**
3. **定期检查日志文件，避免敏感信息泄露**
4. **限制脚本的执行权限**

## 📞 获取帮助

如果遇到问题：

1. 查看 `update.log` 日志文件
2. 检查 `config.py` 配置
3. 验证环境依赖
4. 手动运行 `update_predictions.py` 测试

## 🎯 下一步

设置完成后，你的Kronos预测仪表板将自动保持最新状态！

访问你的GitHub Pages页面查看实时更新的预测结果。