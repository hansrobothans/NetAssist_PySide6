# viewmodels/base_viewmodel.py
"""ViewModel 基类模块.

此模块定义了所有 ViewModel 的基类，提供通用功能。
"""

from PySide6.QtCore import QObject, Signal
from loguru import logger
from typing import Optional


class BaseViewModel(QObject):
    """ViewModel 基类.

    提供所有 ViewModel 的通用功能：
        - 错误处理
        - 状态管理
        - 清理资源
    """

    # 通用信号
    error_occurred = Signal(str)  # (error_message)

    def __init__(self, parent: Optional[QObject] = None):
        """初始化基类.

        :param parent: 父对象
        :type parent: QObject, optional
        """
        logger.trace(f"")
        super().__init__(parent)
        logger.trace(f"初始化{self.__class__.__name__}")

    def emit_error(self, error_message: str):
        """发射错误信号.

        :param error_message: 错误消息
        :type error_message: str
        """
        logger.trace(f"")
        logger.error(f"{self.__class__.__name__}: {error_message}")
        self.error_occurred.emit(error_message)

    def cleanup(self):
        """清理资源.

        子类应该重写此方法以实现特定的清理逻辑。
        """
        logger.trace(f"")
        logger.debug(f"清理{self.__class__.__name__}资源")
        pass

    def __del__(self):
        """析构函数."""
        logger.trace(f"")
        logger.debug(f"{self.__class__.__name__} 析构")
