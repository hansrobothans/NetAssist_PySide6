# views/tabs/placeholder_tab.py
"""占位标签页基类.

为尚未实现的功能提供统一的占位界面。
"""

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from loguru import logger

if TYPE_CHECKING:
    from models.theme_data import ThemeData


class PlaceholderTab(QWidget):
    """占位标签页.

    显示功能名称和"开发中"提示。
    """

    def __init__(self, title: str, description: str = ""):
        super().__init__()
        self._title = title
        self._description = description or f"{title} - 功能开发中"
        self._init_ui()
        logger.info(f"标签页已创建: {title}")

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self._title_label = QLabel(self._title)
        self._title_label.setAlignment(Qt.AlignCenter)
        self._title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(self._title_label)

        self._desc_label = QLabel(self._description)
        self._desc_label.setAlignment(Qt.AlignCenter)
        self._desc_label.setStyleSheet("font-size: 14px; color: #888; margin-top: 8px;")
        layout.addWidget(self._desc_label)

    def apply_theme(self, theme: "ThemeData"):
        """应用主题颜色.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self._title_label.setStyleSheet(
            f"font-size: 24px; font-weight: bold; color: {theme.placeholder_title_color};"
        )
        self._desc_label.setStyleSheet(
            f"font-size: 14px; color: {theme.placeholder_desc_color}; margin-top: 8px;"
        )
