#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kronos自动更新配置文件
"""

# Git配置
GIT_CONFIG = {
    # 主分支名称（通常是 'main' 或 'master'）
    'main_branch': 'main',
    
    # 远程仓库名称
    'remote_name': 'origin',
    
    # 提交信息模板
    'commit_message_template': 'Auto update predictions - {timestamp}',
    
    # 是否在没有变更时也尝试推送
    'push_even_if_no_changes': False
}

# 日志配置
LOG_CONFIG = {
    # 日志文件名
    'log_file': 'update.log',
    
    # 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    'log_level': 'INFO',
    
    # 是否同时输出到控制台
    'console_output': True,
    
    # 日志文件最大大小（MB）
    'max_log_size_mb': 10,
    
    # 保留的日志文件数量
    'backup_count': 5
}

# 预测更新配置
PREDICTION_CONFIG = {
    # 预测脚本文件名
    'prediction_script': 'update_predictions.py',
    
    # 超时时间（秒）
    'timeout_seconds': 300,
    
    # 失败重试次数
    'retry_count': 2,
    
    # 重试间隔（秒）
    'retry_delay': 30
}

# 通知配置（可选）
NOTIFICATION_CONFIG = {
    # 是否启用通知
    'enabled': False,
    
    # 通知方式: 'email', 'webhook', 'none'
    'method': 'none',
    
    # 邮件配置（如果使用邮件通知）
    'email': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': '',
        'password': '',
        'to_address': '',
        'subject': 'Kronos预测更新通知'
    },
    
    # Webhook配置（如果使用webhook通知）
    'webhook': {
        'url': '',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'}
    }
}

# 调度配置（用于定时任务参考）
SCHEDULE_CONFIG = {
    # 推荐的运行间隔（分钟）
    'recommended_interval_minutes': 60,
    
    # 运行时间窗口（24小时制）
    'run_time_window': {
        'start_hour': 0,  # 开始时间（小时）
        'end_hour': 23    # 结束时间（小时）
    },
    
    # 是否在周末运行
    'run_on_weekends': True
}