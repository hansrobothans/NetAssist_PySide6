# views/widgets/title_bar.py
"""自定义窗口标题栏组件（WPS/Chrome 风格标签页集成）.

实现无边框窗口的自定义标题栏，包含：
- 标签页（TitleTabBar）直接嵌入标题栏
- "+" 添加标签页按钮
- 最小化、最大化/还原、关闭按钮
- 拖拽移动：使用 Qt 6 的 QWindow.startSystemMove()（支持 Aero Snap）
- 双击最大化/还原（仅空白区域）
"""

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication, QTabBar
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QMouseEvent, QPalette
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray

from resources.icons import ICONS

if TYPE_CHECKING:
    from models.theme_data import ThemeData


class TitleBarButton(QPushButton):
    """标题栏窗口控制按钮."""

    def __init__(self, icon_name: str, tooltip: str = "", parent=None):
        super().__init__(parent)
        self._icon_name = icon_name
        self._icon_color_normal = QColor("#888888")
        self._icon_color_hover = QColor("#ffffff")
        self._icon_color = self._icon_color_normal
        self._hover = False

        self.setToolTip(tooltip)
        self.setFixedSize(46, 32)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("titleBarButton")

    def enterEvent(self, event):
        self._hover = True
        self._icon_color = self._icon_color_hover
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._icon_color = self._icon_color_normal
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self._icon_name not in ICONS:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

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

    def apply_theme(self, theme: "ThemeData"):
        """应用主题颜色.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self._icon_color_normal = QColor(theme.win_btn_icon)
        self._icon_color_hover = QColor(theme.win_btn_icon_hover)
        self._icon_color = self._icon_color_hover if self._hover else self._icon_color_normal
        self.update()


class CloseButton(TitleBarButton):
    """关闭按钮 - 悬停时红色背景."""

    def __init__(self, parent=None):
        super().__init__("window-close", "关闭", parent)
        self.setObjectName("titleBarCloseButton")

    def enterEvent(self, event):
        self._hover = True
        self._icon_color = self._icon_color_hover
        self.update()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        self._hover = False
        self._icon_color = self._icon_color_normal
        self.update()
        QPushButton.leaveEvent(self, event)


class TitleTabBar(QTabBar):
    """标题栏内嵌标签页栏 - 自绘标签页，参照 electerm 风格.

    使用 paintEvent 自绘，避免 QTabBar::tab 样式表级联失效问题。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleTabBar")
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setExpanding(False)
        self.setDrawBase(False)
        self.setElideMode(Qt.ElideRight)
        self.setMouseTracking(True)
        self._hover_index = -1

        # 主题颜色（默认浅色）
        self._color_bg = QColor("#f0f0f0")
        self._color_tab_active = QColor("#ffffff")
        self._color_tab_hover = QColor("#e5e5e5")
        self._color_text = QColor("#666666")
        self._color_text_active = QColor("#333333")
        self._color_text_hover = QColor("#444444")
        self._color_accent = QColor("#0078d4")

    def apply_theme(self, theme: "ThemeData"):
        """应用主题颜色.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self._color_bg = QColor(theme.tab_bg)
        self._color_tab_active = QColor(theme.tab_active_bg)
        self._color_tab_hover = QColor(theme.tab_hover_bg)
        self._color_text = QColor(theme.tab_text)
        self._color_text_active = QColor(theme.tab_active_text)
        self._color_text_hover = QColor(theme.tab_hover_bg)  # hover 文字用稍亮色
        self._color_accent = QColor(theme.tab_accent)
        self.update()

    def paintEvent(self, event):
        """自绘标签页背景和文字."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 绘制整体背景
        painter.fillRect(self.rect(), self._color_bg)

        for i in range(self.count()):
            rect = self.tabRect(i)
            is_selected = (i == self.currentIndex())
            is_hovered = (i == self._hover_index and not is_selected)

            # 标签页背景
            if is_selected:
                painter.fillRect(rect, self._color_tab_active)
                # 选中标签顶部蓝色指示条
                painter.fillRect(rect.x(), rect.y(), rect.width(), 2, self._color_accent)
                painter.setPen(self._color_text_active)
            elif is_hovered:
                painter.fillRect(rect, self._color_tab_hover)
                painter.setPen(self._color_text_hover)
            else:
                painter.setPen(self._color_text)

            # 绘制文字（右侧留出关闭按钮空间）
            text_rect = rect.adjusted(12, 2, -24, 0)
            elided = painter.fontMetrics().elidedText(
                self.tabText(i), Qt.TextElideMode.ElideRight, text_rect.width()
            )
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

        painter.end()

    def mouseMoveEvent(self, event: QMouseEvent):
        """跟踪悬停标签页索引，空白区域交给父级."""
        index = self.tabAt(event.position().toPoint())
        if index != self._hover_index:
            self._hover_index = index
            self.update()
        if index >= 0:
            super().mouseMoveEvent(event)
        else:
            event.ignore()

    def leaveEvent(self, event):
        """鼠标离开时清除悬停状态."""
        self._hover_index = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """点击 tab 时正常处理，点击空白区域交给父级处理拖拽."""
        index = self.tabAt(event.position().toPoint())
        if index >= 0:
            super().mousePressEvent(event)
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """双击空白区域交给父级处理."""
        index = self.tabAt(event.position().toPoint())
        if index >= 0:
            super().mouseDoubleClickEvent(event)
        else:
            event.ignore()


class AddTabButton(TitleBarButton):
    """标题栏中的 "+" 添加标签页按钮."""

    def __init__(self, parent=None):
        super().__init__("plus", "添加标签页", parent)
        self.setObjectName("addTabButton")
        self.setFixedSize(32, 32)


class TitleBar(QWidget):
    """自定义窗口标题栏（WPS/Chrome 风格）.

    标签页直接嵌入标题栏区域，与窗口控制按钮同行。
    拖拽移动使用 Qt 6 的 QWindow.startSystemMove()，
    支持 Windows Aero Snap（拖到顶部全屏、拖到边缘半屏）。
    """

    add_tab_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._window = None

        self.setFixedHeight(32)
        self.setObjectName("titleBar")

        # QWidget 子类必须设置此属性才能响应样式表的 background-color
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标签页栏
        self.tab_bar = TitleTabBar(self)
        layout.addWidget(self.tab_bar)

        # "+" 添加按钮
        self._btn_add = AddTabButton(self)
        self._btn_add.clicked.connect(self.add_tab_clicked.emit)
        layout.addWidget(self._btn_add)

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

    def apply_theme(self, theme: "ThemeData"):
        """应用主题到标题栏及其所有子组件.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self.tab_bar.apply_theme(theme)
        self._btn_add.apply_theme(theme)
        self.btn_minimize.apply_theme(theme)
        self.btn_maximize.apply_theme(theme)
        self.btn_close.apply_theme(theme)

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
        else:
            win.showMaximized()

    def _on_close(self):
        self._get_window().close()

    def _is_blank_area(self, pos):
        """判断点击位置是否为标题栏空白区域（非子控件）."""
        child = self.childAt(pos)
        if child is None:
            return True
        # tab_bar 内部空白区域也算标题栏空白
        if child is self.tab_bar:
            tab_pos = self.tab_bar.mapFromParent(pos)
            if self.tab_bar.tabAt(tab_pos) < 0:
                return True
        return False

    # --- 拖拽移动（Qt 6 原生 API，支持 Aero Snap） ---

    _drag_start_pos = None      # 最大化拖拽起始全局坐标
    _drag_start_ratio = 0.0     # 鼠标在标题栏的水平比例
    _manual_drag_offset = None  # 手动拖拽时光标相对窗口左上角的偏移

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            if not self._is_blank_area(pos):
                super().mousePressEvent(event)
                return

            win = self._get_window()
            if win and win.windowHandle():
                if win.isMaximized():
                    self._drag_start_pos = event.globalPosition().toPoint()
                    self._drag_start_ratio = event.position().x() / self.width()
                else:
                    win.windowHandle().startSystemMove()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        # 最大化状态下检测拖拽 → 还原窗口并切换到手动拖拽
        if self._drag_start_pos is not None:
            win = self._get_window()
            if win and win.isMaximized():
                delta = event.globalPosition().toPoint() - self._drag_start_pos
                if abs(delta.x()) > 4 or abs(delta.y()) > 4:
                    normal_width = win.normalGeometry().width()

                    win.showNormal()
                    QApplication.processEvents()

                    cursor = event.globalPosition().toPoint()
                    new_x = cursor.x() - int(self._drag_start_ratio * normal_width)
                    new_y = cursor.y() - int(event.position().y())
                    win.move(new_x, new_y)

                    self._manual_drag_offset = cursor - win.pos()
                    self._drag_start_pos = None
            event.accept()
            return

        # 手动拖拽中：跟随鼠标移动窗口
        if self._manual_drag_offset is not None:
            win = self._get_window()
            if win:
                cursor = event.globalPosition().toPoint()
                win.move(cursor - self._manual_drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_start_pos = None
        self._manual_drag_offset = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            if self._is_blank_area(pos):
                self._on_maximize()
                event.accept()
