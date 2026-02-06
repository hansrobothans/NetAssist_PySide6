# services/config/defaults.py
"""默认程序配置模块.

本模块定义了应用程序的默认配置常量。
"""

#: 默认程序配置字典
DEFAULT_CONFIG = {


    # 输出路径配置
    "output": {
        # 是否自动生成基于时间戳的输出目录
        "auto_generate": True,

        # 输出根目录（相对路径或绝对路径）
        # 当 auto_generate=True 时，会在此目录下创建时间戳子目录
        # 当 auto_generate=False 时，直接使用此目录作为输出根目录
        "root_dir": "./resources/output",

        # 手动指定的输出目录（仅在 auto_generate=False 时使用）
        # 如果为 null，则使用 root_dir
        "manual_dir": None,

        # 子目录配置
        "subdirs": {
            "logs": "logs",
        }
    },

    # 日志配置
    "logging": {
        # 全局日志级别: TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
        "level": "INFO",

        # 控制台日志配置
        "console": {
            # 是否输出日志到控制台
            "enabled": True,

            # 控制台日志是否使用颜色
            "colorize": True,

            # 控制台日志格式
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        },

        # 日志文件列表，可配置多个日志文件
        "files": [
            {
                # 所有级别的日志文件（TRACE及以上）
                "name": "all",
                # 是否启用此日志文件
                "enabled": True,
                # 日志文件名（相对于 logs 目录）
                "filename": "all.log",
                # 记录所有级别的日志（TRACE及以上）
                "level": "TRACE",
                # 每10MB轮转一次
                "rotation": "10 MB",
                # 保留7天
                "retention": "7 days",
                # 压缩为zip格式
                "compression": "zip",
                # 文件日志格式（不包含颜色标记）
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
            },
            {
                # INFO及以上级别的日志文件
                "name": "info",
                # 是否启用此日志文件
                "enabled": True,
                # 日志文件名
                "filename": "info.log",
                # 只记录 INFO 及以上级别的日志
                "level": "INFO",
                # 不设置轮转策略
                "rotation": None,
                # 不设置保留时间
                "retention": None,
                # 不压缩
                "compression": None,
                # 文件日志格式
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
            },
            {
                # 错误日志文件
                "name": "error",
                # 是否启用此日志文件
                "enabled": True,
                # 错误日志文件名
                "filename": "error.log",
                # 只记录 ERROR 及以上级别的日志
                "level": "ERROR",
                # 不设置轮转策略
                "rotation": None,
                # 错误日志保留 30 天
                "retention": "30 days",
                # 不压缩
                "compression": None,
                # 错误日志格式，包含异常堆栈
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}"
            }
        ],

        # 是否在异常日志中显示完整的堆栈回溯
        "backtrace": True,

        # 是否显示诊断信息（变量值等），调试时可开启
        "diagnose": False
    }
}
