"""应用样式定义.

此模块定义应用程序中使用的所有样式常量和方法。
主题相关的样式通过工厂方法生成，接收 ThemeData 参数。
"""
from typing import TYPE_CHECKING, Optional

from loguru import logger

if TYPE_CHECKING:
    from models.theme_data import ThemeData


class AppStyles:
    """集中管理应用中的所有样式.

    - 状态色（success/danger/warning 等）不随主题变化，保留为类常量
    - 主窗口全局样式、菜单样式等通过静态工厂方法生成
    """

    # ===== 状态色常量（不随主题变化） =====
    COLOR_SUCCESS = "#4CAF50"
    COLOR_SUCCESS_BG = "#e8f5e9"
    COLOR_DANGER = "#f44336"
    COLOR_DANGER_BG = "#ffebee"
    COLOR_WARNING = "#FF9800"
    COLOR_WARNING_BG = "#fff3e0"
    COLOR_INFO = "#2196F3"
    COLOR_INFO_BG = "#e3f2fd"
    COLOR_PRIMARY = "#2196F3"
    COLOR_SECONDARY = "#757575"

    # ===== 按钮样式（状态色驱动，不随主题变化） =====
    BUTTON_START = f"""
        QPushButton {{
            background-color: {COLOR_SUCCESS};
            color: white;
            border: none;
            padding: 10px 30px;
            font-size: 14pt;
            font-weight: bold;
            border-radius: 5px;
            min-height: 40px;
        }}
        QPushButton:hover {{
            background-color: #45a049;
        }}
        QPushButton:pressed {{
            background-color: #3d8b40;
        }}
        QPushButton:disabled {{
            background-color: #cccccc;
            color: #666666;
        }}
    """

    BUTTON_STOP = f"""
        QPushButton {{
            background-color: {COLOR_DANGER};
            color: white;
            border: none;
            padding: 10px 30px;
            font-size: 14pt;
            font-weight: bold;
            border-radius: 5px;
            min-height: 40px;
        }}
        QPushButton:hover {{
            background-color: #da190b;
        }}
        QPushButton:pressed {{
            background-color: #c41408;
        }}
        QPushButton:disabled {{
            background-color: #cccccc;
            color: #666666;
        }}
    """

    BUTTON_NORMAL = f"""
        QPushButton {{
            background-color: {COLOR_PRIMARY};
            color: white;
            border: none;
            padding: 8px 20px;
            font-size: 11pt;
            border-radius: 4px;
            min-height: 30px;
        }}
        QPushButton:hover {{
            background-color: #1976D2;
        }}
        QPushButton:pressed {{
            background-color: #1565C0;
        }}
        QPushButton:disabled {{
            background-color: #cccccc;
            color: #666666;
        }}
    """

    # ===== 传感器测试样式（状态色驱动） =====
    BUTTON_SENSOR_TEST = f"""
        QPushButton {{
            background-color: {COLOR_INFO};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 12pt;
            min-width: 100px;
        }}
        QPushButton:hover {{
            background-color: #1976D2;
        }}
        QPushButton:pressed {{
            background-color: #0D47A1;
        }}
        QPushButton:disabled {{
            background-color: #BDBDBD;
            color: #757575;
        }}
    """

    BUTTON_SENSOR_TEST_STOP = f"""
        QPushButton {{
            background-color: {COLOR_WARNING};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 12pt;
            min-width: 100px;
        }}
        QPushButton:hover {{
            background-color: #F57C00;
        }}
        QPushButton:pressed {{
            background-color: #E65100;
        }}
        QPushButton:disabled {{
            background-color: #BDBDBD;
            color: #757575;
        }}
    """

    LABEL_SENSOR_VALUE_WHITE = f"""
        QLabel {{
            font-size: 14pt;
            font-weight: bold;
            color: #1976D2;
            padding: 5px 10px;
            background-color: {COLOR_INFO_BG};
            border: 1px solid #BBDEFB;
            border-radius: 4px;
            min-width: 120px;
        }}
    """

    LABEL_SENSOR_VALUE_BLACK = f"""
        QLabel {{
            font-size: 14pt;
            font-weight: bold;
            color: #E65100;
            padding: 5px 10px;
            background-color: {COLOR_WARNING_BG};
            border: 1px solid #FFE0B2;
            border-radius: 4px;
            min-width: 120px;
        }}
    """

    LABEL_SENSOR_VALUE_ERROR = f"""
        QLabel {{
            font-size: 14pt;
            font-weight: bold;
            color: {COLOR_DANGER};
            padding: 5px 10px;
            background-color: {COLOR_DANGER_BG};
            border: 1px solid #FFCDD2;
            border-radius: 4px;
            min-width: 120px;
        }}
    """

    LABEL_SENSOR_NAME = """
        QLabel {
            font-size: 11pt;
            font-weight: bold;
        }
    """

    LABEL_SENSOR_TEST_STATUS = """
        QLabel {
            font-size: 10pt;
            color: #666;
            padding: 5px;
        }
    """

    LABEL_SENSOR_TEST_STATUS_ACTIVE = f"""
        QLabel {{
            font-size: 10pt;
            color: {COLOR_INFO};
            padding: 5px;
        }}
    """

    LABEL_SENSOR_TEST_STATUS_SUCCESS = f"""
        QLabel {{
            font-size: 10pt;
            color: {COLOR_SUCCESS};
            padding: 5px;
        }}
    """

    LABEL_SENSOR_TEST_STATUS_ERROR = f"""
        QLabel {{
            font-size: 10pt;
            color: {COLOR_DANGER};
            padding: 5px;
        }}
    """

    LABEL_SENSOR_TEST_STATUS_WARNING = f"""
        QLabel {{
            font-size: 10pt;
            color: {COLOR_WARNING};
            padding: 5px;
        }}
    """

    # ═══════════════════════════════════════════
    #  主题驱动的工厂方法
    # ═══════════════════════════════════════════

    @staticmethod
    def main_window(t: "ThemeData") -> str:
        """生成主窗口全局样式表.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QMainWindow {{
                background-color: {t.window_bg};
            }}
            /* 侧边栏 */
            #sidebar {{
                background-color: {t.sidebar_bg};
                border: none;
            }}
            #sidebarButton {{
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
                padding: 0px;
            }}
            #sidebarButton:hover {{
                background-color: {t.sidebar_hover_bg};
            }}
            #sidebarButton:pressed {{
                background-color: {t.sidebar_hover_bg};
            }}
            /* 通用按钮 */
            QPushButton {{
                background-color: {t.color_success};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
            QPushButton:disabled {{
                background-color: {t.button_disabled_bg};
            }}
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {t.border};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: {t.text_primary};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QComboBox, QSpinBox, QLineEdit {{
                padding: 5px;
                border: 1px solid {t.input_border};
                border-radius: 3px;
                background-color: {t.input_bg};
                color: {t.text_primary};
            }}
            /* 内容区 */
            #contentStack {{
                background-color: {t.content_bg};
                border: none;
            }}
            /* 标题栏 "+" 添加按钮 */
            #addTabButton {{
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
                padding: 0px;
            }}
            #addTabButton:hover {{
                background-color: {t.win_btn_hover_bg};
            }}
            #addTabButton:pressed {{
                background-color: {t.win_btn_hover_bg};
            }}
            /* 标题栏 */
            #titleBar {{
                background-color: {t.titlebar_bg};
                border: none;
            }}
            #titleBarButton {{
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 46px;
                max-width: 46px;
                min-height: 32px;
                max-height: 32px;
                padding: 0px;
            }}
            #titleBarButton:hover {{
                background-color: {t.win_btn_hover_bg};
            }}
            #titleBarButton:pressed {{
                background-color: {t.win_btn_hover_bg};
            }}
            #titleBarCloseButton {{
                background-color: transparent;
                border: none;
                border-radius: 0px;
                min-width: 46px;
                max-width: 46px;
                min-height: 32px;
                max-height: 32px;
                padding: 0px;
            }}
            #titleBarCloseButton:hover {{
                background-color: {t.close_btn_hover_bg};
            }}
            #titleBarCloseButton:pressed {{
                background-color: {t.close_btn_pressed_bg};
            }}
        """

    @staticmethod
    def menu_style(t: "ThemeData") -> str:
        """生成菜单样式表.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QMenu {{
                background-color: {t.menu_bg};
                color: {t.menu_text};
                border: 1px solid {t.menu_border};
                padding: 4px 0;
            }}
            QMenu::item {{
                padding: 6px 24px;
            }}
            QMenu::item:selected {{
                background-color: {t.menu_hover_bg};
                color: {t.text_primary};
            }}
            QMenu::separator {{
                height: 1px;
                background: {t.menu_separator};
                margin: 4px 8px;
            }}
            QMenu::item:disabled {{
                color: {t.menu_disabled_text};
                font-weight: bold;
            }}
        """

    @staticmethod
    def log_text_edit(t: "ThemeData") -> str:
        """生成日志文本框样式.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QTextEdit {{
                background-color: {t.log_bg};
                color: {t.log_text};
                border: 1px solid {t.log_border};
            }}
        """

    @staticmethod
    def label_status(t: "ThemeData") -> str:
        """生成状态标签样式.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QLabel {{
                font-size: 14pt;
                color: {t.text_primary};
                padding: 15px;
                border-radius: 5px;
                border: 2px solid {t.border};
                background-color: {t.window_bg};
            }}
        """

    @staticmethod
    def label_title(t: "ThemeData") -> str:
        """生成标题标签样式.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QLabel {{
                font-size: 13pt;
                font-weight: bold;
                color: {t.text_primary};
                padding: 5px;
            }}
        """

    @staticmethod
    def label_value(t: "ThemeData") -> str:
        """生成值标签样式.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QLabel {{
                font-size: 12pt;
                padding: 5px;
                border: 1px solid {t.input_border};
                background-color: {t.input_bg};
                color: {t.text_primary};
                border-radius: 3px;
            }}
        """

    @staticmethod
    def line_edit(t: "ThemeData") -> str:
        """生成输入框样式.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QLineEdit {{
                padding: 8px;
                border: 2px solid {t.input_border};
                border-radius: 4px;
                font-size: 11pt;
                background-color: {t.input_bg};
                color: {t.text_primary};
            }}
            QLineEdit:focus {{
                border-color: {t.input_focus_border};
            }}
            QLineEdit:disabled {{
                background-color: {t.input_disabled_bg};
                color: {t.input_disabled_text};
            }}
        """

    @staticmethod
    def table_widget(t: "ThemeData") -> str:
        """生成表格样式.

        :param t: 主题数据
        :type t: ThemeData
        :return: QSS 样式字符串
        :rtype: str
        """
        return f"""
            QTableWidget {{
                border: 1px solid {t.border};
                gridline-color: {t.border};
                background-color: {t.content_bg};
                color: {t.text_primary};
                font-size: 10pt;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:selected {{
                background-color: {t.color_primary};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {t.window_bg};
                color: {t.text_primary};
                padding: 8px;
                border: 1px solid {t.border};
                font-weight: bold;
            }}
        """

    @staticmethod
    def get_status_style(bg_color: str, border_color: str = None) -> str:
        """获取动态状态样式.

        :param bg_color: 背景颜色
        :type bg_color: str
        :param border_color: 边框颜色，默认与背景色相同
        :type border_color: str, optional
        :return: 样式字符串
        :rtype: str
        """
        if border_color is None:
            border_color = bg_color

        return f"""
            QLabel {{
                font-size: 14pt;
                color: #333;
                padding: 15px;
                border-radius: 5px;
                border: 2px solid {border_color};
                background-color: {bg_color};
            }}
        """

    @staticmethod
    def get_button_style(bg_color: str, hover_color: str = None, pressed_color: str = None) -> str:
        """获取自定义颜色的按钮样式.

        :param bg_color: 背景颜色
        :type bg_color: str
        :param hover_color: 悬停颜色
        :type hover_color: str, optional
        :param pressed_color: 按下颜色
        :type pressed_color: str, optional
        :return: 样式字符串
        :rtype: str
        """
        if hover_color is None:
            hover_color = bg_color
        if pressed_color is None:
            pressed_color = bg_color

        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                padding: 8px 20px;
                font-size: 11pt;
                border-radius: 4px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """
