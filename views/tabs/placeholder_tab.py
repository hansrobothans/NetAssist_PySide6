# views/tabs/placeholder_tab.py
"""占位标签页基类.

为尚未实现的功能提供统一的占位界面。
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from loguru import logger


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

        title_label = QLabel(self._title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        desc_label = QLabel(self._description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("font-size: 14px; color: #888; margin-top: 8px;")
        layout.addWidget(desc_label)
