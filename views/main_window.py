# views/main_window.py
"""主窗口 - MVVM架构.

此模块实现应用程序的主窗口，采用MVVM架构设计。
参照 electerm 的 UI 布局：左侧工具栏 + 右侧标签页内容区。
"""

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QMenuBar, QMenu, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QPoint
from loguru import logger

import ctypes
import ctypes.wintypes

from .tabs import LogTab
from .tabs.placeholder_tab import PlaceholderTab
from .sidebar import Sidebar
from .sidebar.add_tab_menu import AddTabMenu
from .widgets.title_bar import TitleBar
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

        创建窗口的主要界面元素：侧边栏 + 标题栏 + 标签页。
        无边框窗口，自定义标题栏在右侧顶部。
        """
        logger.trace(f"")

        # 去掉系统标题栏
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
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

        # 主内容区（垂直布局：标题栏 + 标签页）
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 自定义标题栏（内嵌标签页）
        self.title_bar = TitleBar()
        content_layout.addWidget(self.title_bar)

        # 内容区（QStackedWidget，由标题栏 tab_bar 控制切换）
        self.tabs = QStackedWidget()
        self.tabs.setObjectName("contentStack")
        content_layout.addWidget(self.tabs)

        # 连接标题栏 tab_bar 信号
        self.title_bar.tab_bar.currentChanged.connect(self.tabs.setCurrentIndex)
        self.title_bar.tab_bar.tabCloseRequested.connect(self._on_tab_close_requested)

        main_layout.addWidget(content_widget)

        # 添加 Win32 原生窗口样式，启用边缘缩放和 Aero Snap
        self._setup_native_frame()

    def _connect_signals(self):
        """连接侧边栏和标题栏信号."""
        self.sidebar.menu_clicked.connect(self._on_menu_clicked)
        self.sidebar.add_clicked.connect(self._on_add_clicked)
        self.sidebar.bookmark_clicked.connect(self._on_bookmark_clicked)
        self.sidebar.settings_clicked.connect(self._on_settings_clicked)
        self.sidebar.log_clicked.connect(self._on_log_clicked)
        self.sidebar.about_clicked.connect(self._on_about_clicked)

        # 添加标签页菜单
        self._add_tab_menu = AddTabMenu(self)
        self._add_tab_menu.tab_requested.connect(self._create_tab)

        # 标题栏 "+" 按钮 → 弹出添加菜单
        self.title_bar.add_tab_clicked.connect(self._on_add_tab_btn_clicked)

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

    def _on_add_tab_btn_clicked(self):
        """标题栏 '+' 按钮点击处理 - 弹出添加标签页菜单."""
        logger.debug("标题栏添加按钮点击")
        btn = self.title_bar._btn_add
        pos = btn.mapToGlobal(btn.rect().bottomLeft())
        self._add_tab_menu.show(pos)

    def _create_tab(self, tab_type: str):
        """根据类型创建并添加标签页.

        :param tab_type: 标签页类型标识
        """
        tab_name = AddTabMenu.TAB_TYPES.get(tab_type, tab_type)
        tab = PlaceholderTab(tab_name)
        index = self.tabs.addWidget(tab)
        self.title_bar.tab_bar.addTab(tab_name)
        self.title_bar.tab_bar.setCurrentIndex(index)
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
        """日志按钮点击处理 - 创建新的日志标签页."""
        logger.debug("日志按钮点击")
        log_tab = LogTab()
        index = self.tabs.addWidget(log_tab)
        self.title_bar.tab_bar.addTab("日志")
        self.title_bar.tab_bar.setCurrentIndex(index)

    def _on_about_clicked(self):
        """关于按钮点击处理."""
        logger.debug("关于按钮点击")
        self.show_about()

    def _on_tab_close_requested(self, index: int):
        """标签页关闭请求处理.

        :param index: 标签页索引
        """
        widget = self.tabs.widget(index)
        if widget:
            self.tabs.removeWidget(widget)
            widget.deleteLater()
        self.title_bar.tab_bar.removeTab(index)

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
            /* 内容区 QStackedWidget */
            #contentStack {
                background-color: #ffffff;
                border: none;
            }
            /* 标题栏内嵌标签页样式 */
            #titleTabBar {
                background-color: transparent;
            }
            #titleTabBar::tab {
                background-color: #3c3c3c;
                color: #cccccc;
                padding: 6px 12px;
                margin-right: 1px;
                border: none;
                min-width: 80px;
                max-width: 200px;
            }
            #titleTabBar::tab:selected {
                background-color: #1f1f1f;
                color: #ffffff;
            }
            #titleTabBar::tab:hover:!selected {
                background-color: #4a4a4a;
            }
            #titleTabBar::close-button {
                image: none;
                subcontrol-position: right;
                padding: 2px;
            }
            #titleTabBar::close-button:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            /* 标题栏 "+" 添加按钮 */
            #addTabButton {
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
                padding: 0px;
            }
            #addTabButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            #addTabButton:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
            /* 自定义标题栏样式 */
            #titleBar {
                background-color: #2b2b2b;
                border: none;
            }
            #titleBarButton {
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 46px;
                max-width: 46px;
                min-height: 32px;
                max-height: 32px;
                padding: 0px;
            }
            #titleBarButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            #titleBarButton:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
            #titleBarCloseButton {
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 46px;
                max-width: 46px;
                min-height: 32px;
                max-height: 32px;
                padding: 0px;
            }
            #titleBarCloseButton:hover {
                background-color: #e81123;
            }
            #titleBarCloseButton:pressed {
                background-color: #bf0f1d;
            }
        """)

    # ===== 无边框窗口：Windows 原生事件处理 =====

    EDGE_SIZE = 8  # 边缘检测区域像素

    def _setup_native_frame(self):
        """添加 Win32 原生窗口样式，启用边缘缩放和 Aero Snap.

        FramelessWindowHint 去掉了系统标题栏，但同时也去掉了 WS_THICKFRAME，
        导致系统不处理边缘缩放。这里手动加回来，再通过 WM_NCCALCSIZE 阻止
        系统绘制标题栏和边框。
        """
        hwnd = int(self.winId())
        GWL_STYLE = -16
        WS_THICKFRAME = 0x00040000
        WS_MINIMIZEBOX = 0x00020000
        WS_MAXIMIZEBOX = 0x00010000

        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
        style |= WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)

        # 通知系统窗口样式已变更
        SWP_FRAMECHANGED = 0x0020
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_NOZORDER = 0x0004
        ctypes.windll.user32.SetWindowPos(
            hwnd, 0, 0, 0, 0, 0,
            SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER
        )

    def nativeEvent(self, event_type, message):
        """处理 Windows 原生事件.

        - WM_NCCALCSIZE: 让客户区占满窗口（去掉系统标题栏/边框）
        - WM_NCHITTEST: 仅处理边缘缩放（标题栏拖拽由 TitleBar.startSystemMove 处理）
        """
        if event_type == b"windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(int(message))

            # WM_NCCALCSIZE: 客户区占满整个窗口
            if msg.message == 0x0083:
                if msg.wParam:
                    # 最大化时，调整客户区为显示器工作区域（避免超出屏幕）
                    if self.isMaximized():
                        class NCCALCSIZE_PARAMS(ctypes.Structure):
                            _fields_ = [("rgrc", ctypes.wintypes.RECT * 3)]

                        class MONITORINFO(ctypes.Structure):
                            _fields_ = [
                                ("cbSize", ctypes.wintypes.DWORD),
                                ("rcMonitor", ctypes.wintypes.RECT),
                                ("rcWork", ctypes.wintypes.RECT),
                                ("dwFlags", ctypes.wintypes.DWORD),
                            ]

                        params = NCCALCSIZE_PARAMS.from_address(msg.lParam)
                        monitor = ctypes.windll.user32.MonitorFromWindow(
                            msg.hWnd, 2  # MONITOR_DEFAULTTONEAREST
                        )
                        mi = MONITORINFO()
                        mi.cbSize = ctypes.sizeof(MONITORINFO)
                        ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(mi))

                        params.rgrc[0].left = mi.rcWork.left
                        params.rgrc[0].top = mi.rcWork.top
                        params.rgrc[0].right = mi.rcWork.right
                        params.rgrc[0].bottom = mi.rcWork.bottom

                    return True, 0

            # WM_NCHITTEST: 仅处理边缘缩放
            if msg.message == 0x0084:
                x = ctypes.c_short(msg.lParam & 0xFFFF).value
                y = ctypes.c_short((msg.lParam >> 16) & 0xFFFF).value

                pos = self.mapFromGlobal(QPoint(x, y))
                w, h = self.width(), self.height()
                e = self.EDGE_SIZE
                px, py = pos.x(), pos.y()

                on_left = px <= e
                on_right = px >= w - e
                on_top = py <= e
                on_bottom = py >= h - e

                if on_top and on_left:
                    return True, 13     # HTTOPLEFT
                if on_top and on_right:
                    return True, 14     # HTTOPRIGHT
                if on_bottom and on_left:
                    return True, 16     # HTBOTTOMLEFT
                if on_bottom and on_right:
                    return True, 17     # HTBOTTOMRIGHT
                if on_left:
                    return True, 10     # HTLEFT
                if on_right:
                    return True, 11     # HTRIGHT
                if on_top:
                    return True, 12     # HTTOP
                if on_bottom:
                    return True, 15     # HTBOTTOM

                # 非边缘区域一律返回 HTCLIENT，
                # 避免系统将其识别为标题栏触发 Aero Shake 等行为
                return True, 1          # HTCLIENT

        return super().nativeEvent(event_type, message)

    def changeEvent(self, event):
        """窗口状态变化时同步最大化按钮图标."""
        if event.type() == event.Type.WindowStateChange:
            if self.isMaximized():
                self.title_bar.btn_maximize.set_icon_name("window-restore")
                self.title_bar.btn_maximize.setToolTip("还原")
            else:
                self.title_bar.btn_maximize.set_icon_name("window-maximize")
                self.title_bar.btn_maximize.setToolTip("最大化")
        super().changeEvent(event)

    def closeEvent(self, event):
        """窗口关闭事件 - 清理资源.

        :param event: 关闭事件对象
        :type event: QCloseEvent
        """
        logger.trace(f"")
        logger.info("正在关闭主窗口...")

        # 清理各标签页资源


        event.accept()
