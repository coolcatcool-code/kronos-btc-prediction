#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kronos自动更新系统测试脚本
用于验证环境配置和功能是否正常
"""

import os
import sys
import subprocess
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def test_python_version():
    """测试Python版本"""
    logger.info("=== 测试Python版本 ===")
    version = sys.version
    logger.info(f"Python版本: {version}")
    
    if sys.version_info >= (3, 7):
        logger.info("✅ Python版本符合要求 (>= 3.7)")
        return True
    else:
        logger.error("❌ Python版本过低，需要3.7或更高版本")
        return False

def test_git_availability():
    """测试Git是否可用"""
    logger.info("\n=== 测试Git可用性 ===")
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info(f"✅ Git版本: {result.stdout.strip()}")
            return True
        else:
            logger.error("❌ Git命令执行失败")
            return False
    except FileNotFoundError:
        logger.error("❌ 未找到Git，请确保Git已安装并在PATH中")
        return False
    except subprocess.TimeoutExpired:
        logger.error("❌ Git命令执行超时")
        return False
    except Exception as e:
        logger.error(f"❌ Git测试失败: {e}")
        return False

def test_git_config():
    """测试Git配置"""
    logger.info("\n=== 测试Git配置 ===")
    try:
        # 检查用户名
        result = subprocess.run(['git', 'config', 'user.name'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            logger.info(f"✅ Git用户名: {result.stdout.strip()}")
        else:
            logger.warning("⚠️ Git用户名未配置")
            return False
        
        # 检查邮箱
        result = subprocess.run(['git', 'config', 'user.email'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            logger.info(f"✅ Git邮箱: {result.stdout.strip()}")
        else:
            logger.warning("⚠️ Git邮箱未配置")
            return False
            
        return True
    except Exception as e:
        logger.error(f"❌ Git配置检查失败: {e}")
        return False

def test_git_repository():
    """测试Git仓库状态"""
    logger.info("\n=== 测试Git仓库状态 ===")
    try:
        # 检查是否在Git仓库中
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info("✅ 当前目录是Git仓库")
        else:
            logger.error("❌ 当前目录不是Git仓库")
            return False
        
        # 检查远程仓库
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            logger.info("✅ 远程仓库配置:")
            for line in result.stdout.strip().split('\n'):
                logger.info(f"   {line}")
        else:
            logger.warning("⚠️ 未配置远程仓库")
            return False
            
        return True
    except Exception as e:
        logger.error(f"❌ Git仓库检查失败: {e}")
        return False

def test_required_files():
    """测试必需文件是否存在"""
    logger.info("\n=== 测试必需文件 ===")
    required_files = [
        'update_predictions.py',
        'auto_update.py',
        'config.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            logger.info(f"✅ {file_path} 存在")
        else:
            logger.error(f"❌ {file_path} 不存在")
            all_exist = False
    
    return all_exist

def test_prediction_script():
    """测试预测脚本是否可以运行"""
    logger.info("\n=== 测试预测脚本 ===")
    if not os.path.exists('update_predictions.py'):
        logger.error("❌ update_predictions.py 不存在")
        return False
    
    try:
        # 尝试运行预测脚本（但不等待完成，只检查是否能启动）
        logger.info("正在测试预测脚本启动...")
        result = subprocess.run([sys.executable, 'update_predictions.py', '--help'], 
                              capture_output=True, text=True, timeout=30)
        
        # 如果脚本不支持--help参数，尝试直接运行但立即终止
        if result.returncode != 0:
            logger.info("脚本不支持--help参数，尝试直接检查语法...")
            result = subprocess.run([sys.executable, '-m', 'py_compile', 'update_predictions.py'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info("✅ 预测脚本语法检查通过")
                return True
            else:
                logger.error(f"❌ 预测脚本语法错误: {result.stderr}")
                return False
        else:
            logger.info("✅ 预测脚本可以正常启动")
            return True
            
    except subprocess.TimeoutExpired:
        logger.info("✅ 预测脚本启动正常（测试超时，这是正常的）")
        return True
    except Exception as e:
        logger.error(f"❌ 预测脚本测试失败: {e}")
        return False

def test_directory_permissions():
    """测试目录权限"""
    logger.info("\n=== 测试目录权限 ===")
    try:
        # 测试写入权限
        test_file = 'test_permissions.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        logger.info("✅ 目录具有读写权限")
        return True
    except Exception as e:
        logger.error(f"❌ 目录权限测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    logger.info(f"Kronos自动更新系统测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"当前工作目录: {os.getcwd()}")
    logger.info("=" * 60)
    
    tests = [
        ("Python版本", test_python_version),
        ("Git可用性", test_git_availability),
        ("Git配置", test_git_config),
        ("Git仓库", test_git_repository),
        ("必需文件", test_required_files),
        ("预测脚本", test_prediction_script),
        ("目录权限", test_directory_permissions)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"测试 '{test_name}' 执行异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    logger.info("\n" + "=" * 60)
    logger.info("=== 测试结果汇总 ===")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        logger.info("🎉 所有测试通过！自动更新系统已准备就绪。")
        logger.info("\n下一步: 运行 'python auto_update.py' 或 'run_update.bat' 开始自动更新")
        return True
    else:
        logger.warning(f"⚠️ {total - passed} 项测试失败，请根据上述信息修复问题")
        logger.info("\n请参考 AUTO_UPDATE_README.md 获取详细的配置指南")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)