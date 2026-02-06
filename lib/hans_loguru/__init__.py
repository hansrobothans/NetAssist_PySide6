"""hans_loguru 日志记录包.

提供支持多进程的日志记录功能，可选的UI组件支持。
"""

from .hans_loguru import HansLoguru, LogFileConfig, ConsoleConfig

# 尝试导入UI支持模块（可选依赖）
try:
    from .hans_loguru_ui import HansLoguruUI
    _ui_available = True
except ImportError:
    # 如果 PySide6 未安装或其他依赖缺失，UI 支持不可用
    HansLoguruUI = None
    _ui_available = False

__all__ = [
    'HansLoguru',
    'LogFileConfig',
    'ConsoleConfig',
    'HansLoguruUI',
]


def initialize():
    """包初始化函数.

    执行包级别的初始化操作。
    """
    pass


initialize()


def is_ui_available() -> bool:
    """检查UI组件是否可用.

    :return: UI组件是否可用
    :rtype: bool
    """
    return _ui_available