# viewmodels/theme_viewmodel.py
"""主题 ViewModel.

职责：
    - 封装 ThemeService，提供 Qt 信号
    - View 层通过连接 theme_changed 信号响应主题切换
"""

from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import Signal
from loguru import logger

from viewmodels.base_viewmodel import BaseViewModel
from models.theme_data import ThemeData

if TYPE_CHECKING:
    from services.core.theme import ThemeService


class ThemeViewModel(BaseViewModel):
    """主题 ViewModel.

    信号：
        theme_changed(ThemeData): 主题变更时发射，携带新的主题数据
    """

    theme_changed = Signal(object)  # ThemeData (用 object 避免 PySide6 注册问题)

    def __init__(self, theme_service: "ThemeService", parent=None):
        """初始化主题 ViewModel.

        :param theme_service: 主题服务实例
        :type theme_service: ThemeService
        :param parent: 父 QObject
        """
        super().__init__(parent)
        self._service = theme_service
        logger.trace("ThemeViewModel 已初始化")

    @property
    def current_theme(self) -> ThemeData:
        """获取当前主题."""
        return self._service.current_theme

    @property
    def theme_name(self) -> str:
        """获取当前主题名称."""
        return self._service.theme_name

    def set_theme(self, name: str) -> None:
        """设置主题并通知所有 View.

        :param name: 主题名称
        :type name: str
        """
        try:
            theme = self._service.set_theme(name)
            self.theme_changed.emit(theme)
        except ValueError as e:
            self.emit_error(str(e))

    def toggle_theme(self) -> None:
        """切换主题并通知所有 View."""
        theme = self._service.toggle_theme()
        self.theme_changed.emit(theme)
