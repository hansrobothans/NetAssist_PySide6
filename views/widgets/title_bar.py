# views/widgets/title_bar.py
"""自定义窗口标题栏组件.

实现无边框窗口的自定义标题栏，包含：
- 窗口标题
- 最小化、最大化/还原、关闭按钮
- 拖拽移动窗口
- 双击最大化/还原
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint, QRectF
from PySide6.QtGui import QPainter, QColor, QMouseEvent
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray

from resources.icons import ICONS


class TitleBarButton(QPushButton):
    """标题栏窗口控制按钮."""

    def __init__(self, icon_name: str, tooltip: str = "", parent=None):
        super().__init__(parent)
        self._icon_name = icon_name
        self._icon_color = QColor("#888888")
        self._hover = False

        self.setToolTip(tooltip)
        self.setFixedSize(46, 32)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("titleBarButton")

    def enterEvent(self, event):
        self._hover = True
        self._icon_color = QColor("#ffffff")
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._icon_color = QColor("#888888")
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self._icon_name not in ICONS:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        svg_str = ICONS[self._icon_name]
        svg_str = svg_str.replace('fill="currentColor"', f'fill="{self._icon_color.name()}"')

        svg_data = QByteArray(svg_str.encode('utf-8'))
        renderer = QSvgRenderer(svg_data)

        icon_size = 14
        x = (self.width() - icon_size) // 2
        y = (self.height() - icon_size) // 2
        renderer.render(painter, QRectF(x, y, icon_size, icon_size))

        painter.end()

    def set_icon_name(self, icon_name: str):
        """更新图标名称."""
        self._icon_name = icon_name
        self.update()


class CloseButton(TitleBarButton):
    """关闭按钮 - 悬停时红色背景."""

    def __init__(self, parent=None):
        super().__init__("window-close", "关闭", parent)
        self.setObjectName("titleBarCloseButton")

    def enterEvent(self, event):
        self._hover = True
        self._icon_color = QColor("#ffffff")
        self.update()
        # 跳过 TitleBarButton.enterEvent，直接调用 QPushButton
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        self._hover = False
        self._icon_color = QColor("#888888")
        self.update()
        QPushButton.leaveEvent(self, event)


class TitleBar(QWidget):
    """自定义窗口标题栏."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._window = None
        self._dragging = False
        self._drag_pos = QPoint()

        self.setFixedHeight(32)
        self.setObjectName("titleBar")

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)

        # 标题文字
        self._title_label = QLabel("")
        self._title_label.setObjectName("titleBarLabel")
        layout.addWidget(self._title_label)

        # 弹性空间
        layout.addStretch()

        # 最小化按钮
        self.btn_minimize = TitleBarButton("window-minimize", "最小化")
        self.btn_minimize.clicked.connect(self._on_minimize)
        layout.addWidget(self.btn_minimize)

        # 最大化/还原按钮
        self.btn_maximize = TitleBarButton("window-maximize", "最大化")
        self.btn_maximize.clicked.connect(self._on_maximize)
        layout.addWidget(self.btn_maximize)

        # 关闭按钮
        self.btn_close = CloseButton()
        self.btn_close.clicked.connect(self._on_close)
        layout.addWidget(self.btn_close)

    def set_title(self, title: str):
        """设置标题文字."""
        self._title_label.setText(title)

    def _get_window(self):
        """获取顶层窗口."""
        if self._window is None:
            self._window = self.window()
        return self._window

    def _on_minimize(self):
        self._get_window().showMinimized()

    def _on_maximize(self):
        win = self._get_window()
        if win.isMaximized():
            win.showNormal()
            self.btn_maximize.set_icon_name("window-maximize")
            self.btn_maximize.setToolTip("最大化")
        else:
            win.showMaximized()
            self.btn_maximize.set_icon_name("window-restore")
            self.btn_maximize.setToolTip("还原")

    def _on_close(self):
        self._get_window().close()

    # --- 拖拽移动窗口 ---

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_pos = event.globalPosition().toPoint() - self._get_window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging and event.buttons() & Qt.LeftButton:
            win = self._get_window()
            # 拖拽时如果是最大化状态，先还原
            if win.isMaximized():
                win.showNormal()
                self.btn_maximize.set_icon_name("window-maximize")
                self.btn_maximize.setToolTip("最大化")
                # 重新计算拖拽位置，让鼠标在标题栏中间
                self._drag_pos = QPoint(win.width() // 2, self.height() // 2)
            win.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._dragging = False
        event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._on_maximize()
            event.accept()
