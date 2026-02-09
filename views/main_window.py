# views/main_window.py
"""主窗口 - MVVM架构.

此模块实现应用程序的主窗口，采用MVVM架构设计。
参照 electerm 的 UI 布局：左侧工具栏 + 右侧标签页内容区。
"""

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QMenuBar, QMenu, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from loguru import logger

from .tabs import LogTab
from .tabs.placeholder_tab import PlaceholderTab
from .sidebar import Sidebar
from .sidebar.add_tab_menu import AddTabMenu
from version import APP_TITLE

if TYPE_CHECKING:
    from services import ServiceContainer


class MainWindow(QMainWindow):
    """主窗口 - MVVM架构.

    主窗口包含以下功能：
        - 左侧工具栏（侧边栏）
        - 右侧多标签页界面
        - 管理各个功能模块
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

        # 连接信号
        self._connect_signals()

        logger.info("主窗口初始化完成")

    def init_ui(self):
        """初始化UI.

        创建窗口的主要界面元素：侧边栏 + 标签页。
        """
        logger.trace(f"")
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 1400, 800)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 水平布局：侧边栏 | 主内容区
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 侧边栏
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # 主内容区（垂直布局）
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 创建标签页
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._on_tab_close_requested)
        content_layout.addWidget(self.tabs)

        main_layout.addWidget(content_widget)

        # 日志标签页
        self.log_tab = LogTab()
        self.tabs.addTab(self.log_tab, "日志")

    def _connect_signals(self):
        """连接侧边栏信号."""
        self.sidebar.menu_clicked.connect(self._on_menu_clicked)
        self.sidebar.add_clicked.connect(self._on_add_clicked)
        self.sidebar.bookmark_clicked.connect(self._on_bookmark_clicked)
        self.sidebar.settings_clicked.connect(self._on_settings_clicked)
        self.sidebar.log_clicked.connect(self._on_log_clicked)
        self.sidebar.about_clicked.connect(self._on_about_clicked)

        # 添加标签页菜单
        self._add_tab_menu = AddTabMenu(self)
        self._add_tab_menu.tab_requested.connect(self._create_tab)

    def _on_menu_clicked(self):
        """菜单按钮点击处理."""
        logger.debug("菜单按钮点击")
        # TODO: 显示菜单面板

    def _on_add_clicked(self):
        """添加按钮点击处理 - 弹出添加标签页菜单."""
        logger.debug("添加按钮点击")
        # 在添加按钮右侧弹出菜单
        btn = self.sidebar.btn_add
        pos = btn.mapToGlobal(btn.rect().topRight())
        self._add_tab_menu.show(pos)

    def _create_tab(self, tab_type: str):
        """根据类型创建并添加标签页.

        :param tab_type: 标签页类型标识
        """
        tab_name = AddTabMenu.TAB_TYPES.get(tab_type, tab_type)
        tab = PlaceholderTab(tab_name)
        index = self.tabs.addTab(tab, tab_name)
        self.tabs.setCurrentIndex(index)
        logger.info(f"已添加标签页: {tab_name}")

    def _on_bookmark_clicked(self):
        """收藏按钮点击处理."""
        logger.debug("收藏按钮点击")
        # TODO: 显示收藏面板

    def _on_settings_clicked(self):
        """设置按钮点击处理."""
        logger.debug("设置按钮点击")
        # TODO: 显示设置面板

    def _on_log_clicked(self):
        """日志按钮点击处理 - 切换到日志标签页."""
        logger.debug("日志按钮点击")
        index = self.tabs.indexOf(self.log_tab)
        if index >= 0:
            self.tabs.setCurrentIndex(index)

    def _on_about_clicked(self):
        """关于按钮点击处理."""
        logger.debug("关于按钮点击")
        self.show_about()

    def _on_tab_close_requested(self, index: int):
        """标签页关闭请求处理.

        :param index: 标签页索引
        """
        # 日志标签页不允许关闭
        if self.tabs.widget(index) == self.log_tab:
            return
        self.tabs.removeTab(index)

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
        """应用样式 - 参照 electerm 风格.

        设置全局样式表，侧边栏使用 electerm 的深色主题。
        """
        logger.trace(f"")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            /* 侧边栏样式 - 参照 electerm sidebar.styl */
            #sidebar {
                background-color: #1f1f1f;
                border: none;
            }
            #sidebarButton {
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
                padding: 0px;
            }
            #sidebarButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            #sidebarButton:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
            /* 通用按钮样式 */
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
            /* 标签页样式 */
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
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
