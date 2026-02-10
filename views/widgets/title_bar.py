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
from PySide6.QtCore import Qt, QRectF, Signal, QSize
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

    tab_count_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleTabBar")
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setExpanding(False)
        self.setDrawBase(False)
        self.setElideMode(Qt.ElideRight)
        self.setMouseTracking(True)
        self.setUsesScrollButtons(False)
        self._hover_index = -1

        # 主题颜色（默认浅色）
        self._color_bg = QColor("#f0f0f0")
        self._color_tab_active = QColor("#ffffff")
        self._color_tab_hover = QColor("#e5e5e5")
        self._color_text = QColor("#666666")
        self._color_text_active = QColor("#333333")
        self._color_text_hover = QColor("#444444")
        self._color_accent = QColor("#0078d4")
        self._color_badge_bg = QColor("#0078d4")
        self._color_badge_text = QColor("#ffffff")

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
        self._color_text_hover = QColor(theme.tab_active_text)  # hover 文字用活动标签文字色
        self._color_accent = QColor(theme.tab_accent)
        self._color_badge_bg = QColor(theme.tab_accent)
        self._color_badge_text = QColor("#ffffff")
        self.update()

    def tabSizeHint(self, index):
        """增加标签宽度以容纳编号徽章和类型图标."""
        hint = super().tabSizeHint(index)
        # 额外宽度: 徽章(~18) + 间距(4) + 图标(14) + 间距(4) - 原左边距调整(~2)
        hint.setWidth(hint.width() + 38)
        return hint

    def _tabs_total_width(self):
        """计算所有标签页的自然总宽度（不受控件压缩影响）."""
        total = 0
        for i in range(self.count()):
            total += self.tabSizeHint(i).width()
        return total

    def sizeHint(self):
        """根据实际标签宽度返回精确尺寸，消除多余间距."""
        hint = super().sizeHint()
        hint.setWidth(self._tabs_total_width())
        return hint

    def minimumSizeHint(self):
        """返回最小尺寸提示 - 允许容器压缩标签页栏."""
        hint = super().minimumSizeHint()
        hint.setWidth(0)
        return hint

    def tabInserted(self, index):
        """标签页插入后通知容器重新计算."""
        super().tabInserted(index)
        self.tab_count_changed.emit()

    def tabRemoved(self, index):
        """标签页移除后通知容器重新计算."""
        super().tabRemoved(index)
        self.tab_count_changed.emit()

    def paintEvent(self, event):
        """自绘标签页背景、编号徽章、类型图标和文字."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 绘制整体背景
        painter.fillRect(self.rect(), self._color_bg)

        for i in range(self.count()):
            rect = self.tabRect(i)
            is_selected = (i == self.currentIndex())
            is_hovered = (i == self._hover_index and not is_selected)

            # ── 标签页背景 ──
            if is_selected:
                painter.fillRect(rect, self._color_tab_active)
                # 选中标签顶部蓝色指示条
                painter.fillRect(rect.x(), rect.y(), rect.width(), 2, self._color_accent)
                text_color = self._color_text_active
            elif is_hovered:
                painter.fillRect(rect, self._color_tab_hover)
                text_color = self._color_text_hover
            else:
                text_color = self._color_text

            # ── 获取标签元数据 ──
            data = self.tabData(i) or {}
            number = data.get("number", i + 1)
            icon_name = data.get("icon", "")

            cursor_x = rect.x() + 10

            # ── 编号徽章（electerm 风格药丸形） ──
            badge_text = str(number)
            badge_font = painter.font()
            badge_font.setPixelSize(10)
            badge_font.setBold(is_selected)
            painter.setFont(badge_font)
            badge_text_width = painter.fontMetrics().horizontalAdvance(badge_text)
            badge_w = max(badge_text_width + 10, 18)
            badge_h = 14
            badge_y = rect.y() + (rect.height() - badge_h) // 2

            badge_rect = QRectF(cursor_x, badge_y, badge_w, badge_h)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self._color_badge_bg)
            # 左侧圆角大，右侧圆角小（药丸形）
            painter.drawRoundedRect(badge_rect, 7, 7)
            # 右侧覆盖为小圆角
            right_rect = QRectF(cursor_x + badge_w / 2, badge_y, badge_w / 2, badge_h)
            painter.drawRoundedRect(right_rect, 2, 2)

            # 徽章数字
            painter.setPen(self._color_badge_text)
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, badge_text)

            cursor_x += badge_w + 4

            # ── 类型图标 ──
            if icon_name and icon_name in ICONS:
                icon_size = 14
                icon_y = rect.y() + (rect.height() - icon_size) // 2

                svg_str = ICONS[icon_name]
                svg_str = svg_str.replace(
                    'fill="currentColor"', f'fill="{text_color.name()}"'
                )
                svg_data = QByteArray(svg_str.encode('utf-8'))
                renderer = QSvgRenderer(svg_data)
                renderer.render(painter, QRectF(cursor_x, icon_y, icon_size, icon_size))

                cursor_x += icon_size + 4

            # ── 标签文字 ──
            text_font = painter.font()
            text_font.setPixelSize(12)
            text_font.setBold(False)
            painter.setFont(text_font)
            painter.setPen(text_color)

            text_rect = rect.adjusted(0, 2, -24, 0)
            text_rect.setLeft(cursor_x)
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


class TabNavButton(TitleBarButton):
    """标签页导航按钮（滚动左/右、下拉列表）."""

    def __init__(self, icon_name: str, tooltip: str = "", parent=None):
        super().__init__(icon_name, tooltip, parent)
        self.setObjectName("tabNavButton")
        self.setFixedSize(28, 32)


class TabBarScrollContainer(QWidget):
    """标签页栏滚动容器.

    将 TitleTabBar 放入固定高度的容器中，
    当标签页总宽度超过容器宽度时，通过偏移量实现水平滚动。
    """

    overflow_changed = Signal(bool)

    def __init__(self, tab_bar: TitleTabBar, parent=None):
        super().__init__(parent)
        self._tab_bar = tab_bar
        self._scroll_offset = 0
        self._tab_bar.setParent(self)
        self.setFixedHeight(32)

        # 允许布局压缩容器（标签溢出时）
        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self._tab_bar.tab_count_changed.connect(self._on_tabs_changed)

    def sizeHint(self):
        """返回标签页自然总宽度作为首选宽度."""
        return QSize(self._tab_bar._tabs_total_width(), 32)

    def minimumSizeHint(self):
        """允许容器被压缩到任意宽度."""
        return QSize(0, 32)

    def is_overflowing(self):
        """标签页总宽度是否超过容器宽度."""
        return self._tab_bar._tabs_total_width() > self.width()

    def scroll_left(self):
        """向左滚动（显示更左边的标签页）."""
        self._scroll_offset = max(0, self._scroll_offset - 120)
        self._update_tab_bar_position()

    def scroll_right(self):
        """向右滚动（显示更右边的标签页）."""
        max_offset = max(0, self._tab_bar._tabs_total_width() - self.width())
        self._scroll_offset = min(max_offset, self._scroll_offset + 120)
        self._update_tab_bar_position()

    def ensure_current_visible(self):
        """确保当前选中的标签页可见."""
        index = self._tab_bar.currentIndex()
        if index < 0:
            return
        tab_rect = self._tab_bar.tabRect(index)
        tab_left = tab_rect.x()
        tab_right = tab_left + tab_rect.width()

        if tab_left < self._scroll_offset:
            self._scroll_offset = tab_left
        elif tab_right > self._scroll_offset + self.width():
            self._scroll_offset = tab_right - self.width()

        self._update_tab_bar_position()

    def _update_tab_bar_position(self):
        """根据滚动偏移量更新标签页栏位置."""
        self._tab_bar.move(-self._scroll_offset, 0)
        self._check_overflow()

    def _check_overflow(self):
        """检查溢出状态并发射信号."""
        self.overflow_changed.emit(self.is_overflowing())

    def _on_tabs_changed(self):
        """标签页数量变化时，重新计算布局."""
        total_w = self._tab_bar._tabs_total_width()
        bar_w = max(self.width(), total_w)
        self._tab_bar.setFixedSize(bar_w, self.height())

        # 修正滚动偏移量（防止越界）
        max_offset = max(0, total_w - self.width())
        self._scroll_offset = min(self._scroll_offset, max_offset)
        self._update_tab_bar_position()

        # 通知父布局重新计算（容器首选宽度已变化）
        self.updateGeometry()

    def resizeEvent(self, event):
        """容器大小变化时，重新布局标签页栏并检查溢出."""
        super().resizeEvent(event)
        total_w = self._tab_bar._tabs_total_width()
        bar_w = max(self.width(), total_w)
        self._tab_bar.setFixedSize(bar_w, self.height())

        # 修正滚动偏移量
        max_offset = max(0, total_w - self.width())
        self._scroll_offset = min(self._scroll_offset, max_offset)
        self._update_tab_bar_position()


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
        self._current_theme = None

        self.setFixedHeight(32)
        self.setObjectName("titleBar")

        # QWidget 子类必须设置此属性才能响应样式表的 background-color
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标签页栏（包裹在滚动容器中）
        self.tab_bar = TitleTabBar(self)
        self._tab_container = TabBarScrollContainer(self.tab_bar, self)
        layout.addWidget(self._tab_container)

        # "+" 添加按钮
        self._btn_add = AddTabButton(self)
        self._btn_add.clicked.connect(self.add_tab_clicked.emit)
        layout.addWidget(self._btn_add)

        # 弹性空间
        layout.addStretch()

        # ── 标签页导航按钮 ──
        self._btn_scroll_left = TabNavButton("chevron-left", "向左滚动")
        self._btn_scroll_left.clicked.connect(self._tab_container.scroll_left)
        layout.addWidget(self._btn_scroll_left)

        self._btn_scroll_right = TabNavButton("chevron-right", "向右滚动")
        self._btn_scroll_right.clicked.connect(self._tab_container.scroll_right)
        layout.addWidget(self._btn_scroll_right)

        self._btn_tab_list = TabNavButton("chevron-down", "标签页列表")
        self._btn_tab_list.clicked.connect(self._show_tab_list)
        layout.addWidget(self._btn_tab_list)

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

        # 标签页变化时确保当前标签可见
        self.tab_bar.currentChanged.connect(self._on_tab_changed)

    def apply_theme(self, theme: "ThemeData"):
        """应用主题到标题栏及其所有子组件.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self._current_theme = theme
        self.tab_bar.apply_theme(theme)
        self._btn_add.apply_theme(theme)
        self._btn_scroll_left.apply_theme(theme)
        self._btn_scroll_right.apply_theme(theme)
        self._btn_tab_list.apply_theme(theme)
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
            tab_pos = self.tab_bar.mapFrom(self, pos)
            if self.tab_bar.tabAt(tab_pos) < 0:
                return True
        # 滚动容器的空白区域也算标题栏空白
        if child is self._tab_container:
            tab_pos = self.tab_bar.mapFrom(self, pos)
            if self.tab_bar.tabAt(tab_pos) < 0:
                return True
        return False

    def _on_tab_changed(self, index: int):
        """标签页切换时，确保当前标签页可见."""
        if index >= 0:
            self._tab_container.ensure_current_visible()

    def _show_tab_list(self):
        """显示所有标签页的下拉列表."""
        from PySide6.QtWidgets import QMenu
        from views.styles.app_styles import AppStyles

        menu = QMenu(self)

        if self._current_theme:
            menu.setStyleSheet(AppStyles.menu_style(self._current_theme))

        current_index = self.tab_bar.currentIndex()

        for i in range(self.tab_bar.count()):
            tab_text = self.tab_bar.tabText(i)
            data = self.tab_bar.tabData(i) or {}
            number = data.get("number", i + 1)
            prefix = f"● {number}. " if i == current_index else f"   {number}. "
            display_text = f"{prefix}{tab_text}"
            action = menu.addAction(display_text)
            action.setData(i)

        pos = self._btn_tab_list.mapToGlobal(
            self._btn_tab_list.rect().bottomLeft()
        )

        selected = menu.exec(pos)
        if selected is not None and selected.data() is not None:
            self.tab_bar.setCurrentIndex(selected.data())

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
