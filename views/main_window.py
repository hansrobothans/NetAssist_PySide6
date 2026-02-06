# views/main_window.py
"""主窗口 - MVVM架构.

此模块实现应用程序的主窗口，采用MVVM架构设计。
"""

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QMenuBar, QMenu, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from loguru import logger

from .tabs import LogTab
from version import APP_TITLE

if TYPE_CHECKING:
    from services import ServiceContainer


class MainWindow(QMainWindow):
    """主窗口 - MVVM架构.

    主窗口包含以下功能：
        - 创建多标签页界面
        - 管理各个功能模块
        - 提供菜单栏和样式设置
        - 处理窗口关闭事件
    """

    def __init__(self, container: "ServiceContainer"):
        """初始化主窗口.

        :param container: 服务容器实例
        :type container: ServiceContainer
        """
        logger.trace(f"")
        super().__init__()

        # 保存服务容器
        self._container = container

        # 初始化UI
        self.init_ui()

        # 应用样式
        self.apply_styles()

        logger.info("主窗口初始化完成")

    def init_ui(self):
        """初始化UI.

        创建窗口的主要界面元素，包括菜单栏和标签页。
        """
        logger.trace(f"")
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 1400, 800)

        # 创建菜单栏
        self.create_menu_bar()

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建标签页
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # 调试助手（MVVM架构）

        # 日志
        self.log_tab = LogTab()
        self.tabs.addTab(self.log_tab, "日志")

    def create_menu_bar(self):
        """创建菜单栏.

        添加帮助菜单和相关菜单项。
        """
        logger.trace(f"")
        menubar = self.menuBar()

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        help_menu.addAction("关于", self.show_about)

    def show_about(self):
        """显示关于对话框.

        弹出对话框显示程序版本和架构信息。
        """
        logger.trace(f"")
        QMessageBox.about(
            self,
            "关于",
            f"{APP_TITLE}\n\n"
            "MVVM架构 + QThread\n"
            "使用Qt信号槽实现数据绑定\n"
        )

    def apply_styles(self):
        """应用样式.

        设置全局样式表，包括按钮、输入框、组框等组件的样式。
        """
        logger.trace(f"")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QComboBox, QSpinBox, QLineEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
        """)

    def closeEvent(self, event):
        """窗口关闭事件 - 清理资源.

        :param event: 关闭事件对象
        :type event: QCloseEvent
        """
        logger.trace(f"")
        logger.info("正在关闭主窗口...")

        # 清理各标签页资源


        event.accept()
