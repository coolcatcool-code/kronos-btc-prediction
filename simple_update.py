#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kronos简化版自动更新脚本
适用于没有Git环境的情况，仅更新预测数据
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simple_update.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_environment():
    """检查运行环境"""
    logger.info("检查运行环境...")
    
    # 检查Python版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    logger.info(f"Python版本: {python_version}")
    
    # 检查工作目录
    cwd = os.getcwd()
    logger.info(f"工作目录: {cwd}")
    
    # 检查预测脚本是否存在
    prediction_script = 'update_predictions.py'
    if not os.path.exists(prediction_script):
        logger.error(f"未找到预测脚本: {prediction_script}")
        return False
    
    logger.info(f"找到预测脚本: {prediction_script}")
    return True

def run_prediction_update():
    """运行预测更新"""
    logger.info("开始更新预测数据...")
    
    try:
        # 运行预测脚本
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, 'update_predictions.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            logger.info(f"预测数据更新成功 (耗时: {duration:.2f}秒)")
            if result.stdout:
                logger.info(f"输出: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"预测数据更新失败 (退出码: {result.returncode})")
            if result.stderr:
                logger.error(f"错误信息: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("预测数据更新超时 (5分钟)")
        return False
    except Exception as e:
        logger.error(f"运行预测更新时发生异常: {e}")
        return False

def check_generated_files():
    """检查生成的文件"""
    logger.info("检查生成的文件...")
    
    expected_files = [
        'prediction_chart_1h.png',
        'prediction_chart_4h.png', 
        'prediction_chart_1d.png'
    ]
    
    generated_files = []
    missing_files = []
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            # 获取文件修改时间
            mtime = os.path.getmtime(file_path)
            mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"✅ {file_path} (修改时间: {mtime_str})")
            generated_files.append(file_path)
        else:
            logger.warning(f"⚠️ {file_path} 未找到")
            missing_files.append(file_path)
    
    if generated_files:
        logger.info(f"成功生成 {len(generated_files)} 个文件")
    
    if missing_files:
        logger.warning(f"缺少 {len(missing_files)} 个预期文件")
    
    return len(generated_files) > 0

def create_update_summary():
    """创建更新摘要"""
    summary_file = 'last_update_summary.txt'
    
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Kronos预测数据更新摘要\n")
            f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"工作目录: {os.getcwd()}\n")
            f.write(f"Python版本: {sys.version.split()[0]}\n")
            f.write("\n生成的文件:\n")
            
            files = ['prediction_chart_1h.png', 'prediction_chart_4h.png', 'prediction_chart_1d.png']
            for file_path in files:
                if os.path.exists(file_path):
                    mtime = os.path.getmtime(file_path)
                    mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                    size = os.path.getsize(file_path)
                    f.write(f"- {file_path} ({size} bytes, {mtime_str})\n")
                else:
                    f.write(f"- {file_path} (未找到)\n")
        
        logger.info(f"更新摘要已保存到: {summary_file}")
        
    except Exception as e:
        logger.error(f"创建更新摘要失败: {e}")

def main():
    """主函数"""
    start_time = datetime.now()
    logger.info(f"=== Kronos简化版自动更新开始 ({start_time.strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    try:
        # 检查环境
        if not check_environment():
            logger.error("环境检查失败，退出")
            return False
        
        # 运行预测更新
        if not run_prediction_update():
            logger.error("预测数据更新失败")
            return False
        
        # 检查生成的文件
        if not check_generated_files():
            logger.warning("未生成预期的文件")
        
        # 创建更新摘要
        create_update_summary()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"=== 简化版自动更新结束 ({end_time.strftime('%Y-%m-%d %H:%M:%S')}) ===")
        logger.info(f"总耗时: {duration:.2f}秒")
        logger.info("状态: 成功")
        
        return True
        
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        return False
    except Exception as e:
        logger.error(f"自动更新过程中发生异常: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)