# views/sidebar/add_tab_menu.py
"""添加标签页菜单 - 点击添加按钮时弹出."""

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal, QObject
from loguru import logger

from views.styles.app_styles import AppStyles

if TYPE_CHECKING:
    from models.theme_data import ThemeData


class AddTabMenu(QObject):
    """添加标签页菜单.

    提供分类的标签页创建选项:
    1. 网络调试助手 (TCP服务端/客户端, UDP服务端/客户端)
    2. 串口助手
    3. I2C助手
    4. SPI助手
    5. GPIO助手
    """

    tab_requested = Signal(str)  # 发送标签页类型标识

    # 标签页类型定义: (类型标识, 显示名称)
    TAB_TYPES = {
        "tcp_server": "TCP服务端助手",
        "tcp_client": "TCP客户端助手",
        "udp_server": "UDP服务端助手",
        "udp_client": "UDP客户端助手",
        "serial": "串口助手",
        "i2c": "I2C助手",
        "spi": "SPI助手",
        "gpio": "GPIO助手",
    }

    # 标签页类型 → 图标名称映射
    TAB_ICONS = {
        "tcp_server": "cloud-server",
        "tcp_client": "send",
        "udp_server": "cloud-server",
        "udp_client": "send",
        "serial": "api",
        "i2c": "chip",
        "spi": "swap",
        "gpio": "toggle",
        "log": "file-text",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme = None

    def apply_theme(self, theme: "ThemeData"):
        """保存当前主题，供下次弹出菜单时使用.

        :param theme: 主题数据
        :type theme: ThemeData
        """
        self._theme = theme

    def show(self, pos):
        """在指定位置显示菜单.

        :param pos: 全局坐标位置
        """
        menu = QMenu()

        if self._theme:
            style = AppStyles.menu_style(self._theme)
        else:
            # 回退默认样式
            style = """
                QMenu {
                    background-color: #2b2b2b;
                    color: #cccccc;
                    border: 1px solid #3c3c3c;
                    padding: 4px 0;
                }
                QMenu::item {
                    padding: 6px 24px;
                }
                QMenu::item:selected {
                    background-color: #3c3c3c;
                    color: #ffffff;
                }
                QMenu::separator {
                    height: 1px;
                    background: #3c3c3c;
                    margin: 4px 8px;
                }
                QMenu::item:disabled {
                    color: #888888;
                    font-weight: bold;
                }
            """
        menu.setStyleSheet(style)

        # 网络调试助手子菜单
        net_menu = menu.addMenu("网络调试助手")
        net_menu.setStyleSheet(style)

        for tab_type in ("tcp_server", "tcp_client", "udp_server", "udp_client"):
            action = net_menu.addAction(self.TAB_TYPES[tab_type])
            action.setData(tab_type)

        menu.addSeparator()

        # 其他助手
        for tab_type in ("serial", "i2c", "spi", "gpio"):
            action = menu.addAction(self.TAB_TYPES[tab_type])
            action.setData(tab_type)

        # 处理选择
        action = menu.exec(pos)
        if action and action.data():
            tab_type = action.data()
            logger.info(f"用户请求添加标签页: {self.TAB_TYPES.get(tab_type, tab_type)}")
            self.tab_requested.emit(tab_type)
