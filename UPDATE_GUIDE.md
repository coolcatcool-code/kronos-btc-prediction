# Kronos 自动更新使用指南

本项目提供了两种自动更新方式，请根据你的环境选择合适的方案。

## 🔄 更新方式对比

| 功能 | 完整版 (auto_update.py) | 简化版 (simple_update.py) |
|------|------------------------|---------------------------|
| 预测数据更新 | ✅ | ✅ |
| Git提交推送 | ✅ | ❌ |
| GitHub自动部署 | ✅ | ❌ |
| 环境要求 | Python + Git | 仅Python |
| 适用场景 | 生产环境 | 本地测试 |

## 🚀 快速开始

### 方案一：简化版（推荐新手）

**适用情况：**
- 没有安装Git
- 只想本地更新预测数据
- 测试功能是否正常

**使用方法：**

1. **直接运行批处理文件**
   ```cmd
   双击 run_simple_update.bat
   ```

2. **或使用命令行**
   ```cmd
   python simple_update.py
   ```

**输出文件：**
- `prediction_chart_1h.png` - 1小时预测图表
- `prediction_chart_4h.png` - 4小时预测图表  
- `prediction_chart_1d.png` - 1天预测图表
- `simple_update.log` - 运行日志
- `last_update_summary.txt` - 更新摘要

### 方案二：完整版（推荐生产环境）

**适用情况：**
- 已安装Git
- 需要自动推送到GitHub
- 希望GitHub Pages自动更新

**前置要求：**
1. 安装Git：[https://git-scm.com/download/windows](https://git-scm.com/download/windows)
2. 配置Git用户信息：
   ```cmd
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```
3. 确保当前目录是Git仓库且已连接到GitHub

**使用方法：**

1. **测试环境**
   ```cmd
   python test_update.py
   ```

2. **运行完整更新**
   ```cmd
   双击 run_update.bat
   # 或
   python auto_update.py
   ```

## 📋 环境检查

### 检查Python环境
```cmd
python --version
```
应该显示Python 3.7或更高版本。

### 检查Git环境（完整版需要）
```cmd
git --version
git config --list
```

### 运行环境测试
```cmd
python test_update.py
```

## 🕐 设置定时任务

### Windows任务计划程序

1. 按 `Win + R`，输入 `taskschd.msc`
2. 创建基本任务
3. 设置触发器（建议每4小时）
4. 设置操作：
   - **简化版**：`C:\path\to\run_simple_update.bat`
   - **完整版**：`C:\path\to\run_update.bat`

### 使用批处理脚本定时运行

创建 `schedule_update.bat`：

```batch
@echo off
:loop
echo %date% %time% - 运行预测更新
call run_simple_update.bat
echo 等待4小时后再次运行...
timeout /t 14400 /nobreak
goto loop
```

## 📊 监控和日志

### 查看日志

**简化版日志：**
```cmd
type simple_update.log
```

**完整版日志：**
```cmd
type update.log
```

### 查看更新摘要
```cmd
type last_update_summary.txt
```

### 日志示例

**简化版成功日志：**
```
2024-01-15 10:00:01,123 - INFO - === Kronos简化版自动更新开始 (2024-01-15 10:00:01) ===
2024-01-15 10:00:01,124 - INFO - 检查运行环境...
2024-01-15 10:00:01,125 - INFO - Python版本: 3.9.7
2024-01-15 10:00:01,126 - INFO - 工作目录: C:\Users\Zero\Kronos-demo-master
2024-01-15 10:00:01,127 - INFO - 找到预测脚本: update_predictions.py
2024-01-15 10:00:01,128 - INFO - 开始更新预测数据...
2024-01-15 10:00:15,456 - INFO - 预测数据更新成功 (耗时: 14.33秒)
2024-01-15 10:00:15,457 - INFO - 检查生成的文件...
2024-01-15 10:00:15,458 - INFO - ✅ prediction_chart_1h.png (修改时间: 2024-01-15 10:00:15)
2024-01-15 10:00:15,459 - INFO - ✅ prediction_chart_4h.png (修改时间: 2024-01-15 10:00:15)
2024-01-15 10:00:15,460 - INFO - ✅ prediction_chart_1d.png (修改时间: 2024-01-15 10:00:15)
2024-01-15 10:00:15,461 - INFO - 成功生成 3 个文件
2024-01-15 10:00:15,462 - INFO - 更新摘要已保存到: last_update_summary.txt
2024-01-15 10:00:15,463 - INFO - === 简化版自动更新结束 (2024-01-15 10:00:15) ===
2024-01-15 10:00:15,464 - INFO - 总耗时: 14.34秒
2024-01-15 10:00:15,465 - INFO - 状态: 成功
```

## 🔧 故障排除

### 常见问题

**1. Python未找到**
```
错误: 未找到Python，请确保Python已安装并在PATH中
```
解决方案：
- 安装Python：[https://www.python.org/downloads/](https://www.python.org/downloads/)
- 安装时勾选"Add Python to PATH"

**2. 预测脚本执行失败**
```
预测数据更新失败 (退出码: 1)
```
解决方案：
- 检查 `update_predictions.py` 是否存在
- 手动运行：`python update_predictions.py`
- 查看错误信息

**3. 权限问题**
```
目录权限测试失败
```
解决方案：
- 以管理员身份运行
- 检查文件夹权限
- 确保有写入权限

**4. Git相关问题（完整版）**
```
未找到Git，请确保Git已安装并在PATH中
```
解决方案：
- 安装Git：[https://git-scm.com/download/windows](https://git-scm.com/download/windows)
- 配置用户信息
- 或使用简化版

### 调试步骤

1. **运行环境测试**
   ```cmd
   python test_update.py
   ```

2. **手动运行预测脚本**
   ```cmd
   python update_predictions.py
   ```

3. **检查生成的文件**
   ```cmd
   dir *.png
   ```

4. **查看详细日志**
   ```cmd
   type simple_update.log
   ```

## 📈 推荐配置

### 运行频率
- **开发测试**：手动运行
- **日常使用**：每4小时
- **高频更新**：每小时（注意资源消耗）

### 文件管理
- 定期清理日志文件（超过10MB时）
- 备份重要的预测图表
- 监控磁盘空间使用

## 🎯 下一步

1. **选择合适的更新方式**
   - 新手或测试：使用简化版
   - 生产环境：配置完整版

2. **设置定时任务**
   - Windows任务计划程序
   - 或批处理循环脚本

3. **监控运行状态**
   - 定期查看日志
   - 验证生成的图表

4. **（可选）配置Git和GitHub**
   - 实现自动部署
   - GitHub Pages自动更新

---

**需要帮助？**
- 查看日志文件获取详细错误信息
- 运行 `python test_update.py` 诊断环境问题
- 参考 `AUTO_UPDATE_README.md` 获取完整版配置指南