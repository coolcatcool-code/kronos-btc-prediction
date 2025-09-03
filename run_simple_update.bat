@echo off
chcp 65001 >nul
echo ====================================
echo    Kronos 简化版预测数据更新工具
echo ====================================
echo.
echo 注意: 此版本仅更新预测数据，不包含Git推送功能
echo 如需完整的Git集成功能，请安装Git后使用 run_update.bat
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

echo Python环境检查通过
echo.

:: 运行简化版自动更新脚本
echo 开始运行简化版自动更新...
echo.
python simple_update.py

:: 检查执行结果
if errorlevel 1 (
    echo.
    echo 自动更新失败，请检查日志文件 simple_update.log
) else (
    echo.
    echo 自动更新完成！
    echo.
    echo 生成的文件:
    if exist "prediction_chart_1h.png" echo   ✅ prediction_chart_1h.png
    if exist "prediction_chart_4h.png" echo   ✅ prediction_chart_4h.png
    if exist "prediction_chart_1d.png" echo   ✅ prediction_chart_1d.png
    echo.
    echo 查看详细信息: simple_update.log
    echo 更新摘要: last_update_summary.txt
)

echo.
echo 按任意键退出...
pause >nul