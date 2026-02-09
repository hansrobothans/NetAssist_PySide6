# views/sidebar/sidebar_button.py
"""侧边栏图标按钮组件 - 参照 electerm 风格."""

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray

from resources.icons import ICONS

if TYPE_CHECKING:
    from models.theme_data import ThemeData


class SidebarButton(QPushButton):
    """侧边栏图标按钮 - 参照 electerm 风格.

    使用 Ant Design Outlined 风格的 SVG 图标。
    """

    def __init__(self, icon_name: str, tooltip: str = "", parent=None):
        """初始化侧边栏按钮.

        :param icon_name: 图标名称 (menu, plus-circle, book, setting, file-text, info-circle)
        :param tooltip: 鼠标悬停提示
        :param parent: 父组件
        """
        super().__init__(parent)

        self._icon_name = icon_name
        self._icon_color_normal = QColor("#888888")
        self._icon_color_hover = QColor("#ffffff")
        self._icon_color = self._icon_color_normal
        self._hover = False

        self.setToolTip(tooltip)
        self.setFixedSize(36, 36)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("sidebarButton")

    def enterEvent(self, event):
        """鼠标进入事件."""
        self._hover = True
        self._icon_color = self._icon_color_hover
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件."""
        self._hover = False
        self._icon_color = self._icon_color_normal
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """绘制事件 - 绘制 SVG 图标."""
        super().paintEvent(event)

        if self._icon_name not in ICONS:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 获取 SVG 并替换颜色
        svg_str = ICONS[self._icon_name]
        svg_str = svg_str.replace('fill="currentColor"', f'fill="{self._icon_color.name()}"')

        # 渲染 SVG
        svg_data = QByteArray(svg_str.encode('utf-8'))
        renderer = QSvgRenderer(svg_data)

        # 居中绘制，图标大小 20x20
        icon_size = 20
        x = (self.width() - icon_size) // 2
        y = (self.height() - icon_size) // 2

        renderer.render(painter, QRectF(x, y, icon_size, icon_size))

        painter.end()

    def apply_theme(self, theme: "ThemeData"):
        """应用主题颜色.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self._icon_color_normal = QColor(theme.sidebar_icon)
        self._icon_color_hover = QColor(theme.sidebar_icon_hover)
        self._icon_color = self._icon_color_hover if self._hover else self._icon_color_normal
        self.update()
