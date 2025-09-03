@echo off
chcp 65001 >nul
echo ====================================
echo    Kronos 预测数据自动更新工具
echo ====================================
echo.

:: 切换到脚本所在目录
cd /d "%~dp0"

:: 显示当前目录
echo 当前工作目录: %CD%
echo.

:: 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请确保Python已安装并在PATH中
    pause
    exit /b 1
)

:: 检查Git是否可用
git --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Git，请确保Git已安装并在PATH中
    pause
    exit /b 1
)

:: 运行自动更新脚本
echo 开始运行自动更新...
echo.
python auto_update.py

:: 检查执行结果
if errorlevel 1 (
    echo.
    echo 自动更新失败，请检查日志文件 update.log
) else (
    echo.
    echo 自动更新完成！
)

echo.
echo 按任意键退出...
pause >nul