# ui/tabs/log_tab.py
"""日志标签页.

此模块实现日志显示标签页，使用HansLoguru UI组件。
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from loguru import logger
from views.widgets.log_widget import LogWidget


class LogTab(QWidget):
    """日志标签页 - 使用 HansLoguru UI 组件.

    提供日志的实时显示功能。
    """

    def __init__(self):
        logger.trace(f"")
        super().__init__()

        self.init_ui()

        logger.info("日志标签页已初始化")

    def init_ui(self):
        """初始化UI.

        创建日志显示组件并配置显示选项。
        """
        logger.trace(f"")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # 使用 HansLoguru 的 LogWidget 组件
        self.log_widget = LogWidget(
            parent=self,
            default_filter_level="TRACE",  # 默认显示所有级别
            auto_register=True,             # 自动注册到 loguru
            dark_theme=True                 # 使用深色主题
        )

        layout.addWidget(self.log_widget)

    def apply_theme(self, theme):
        """应用主题到日志标签页.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self.log_widget.apply_theme(theme)