"""应用样式定义.

此模块定义应用程序中使用的所有样式常量和方法。
"""
from typing import Optional, Tuple
from loguru import logger


class AppStyles:
    """集中管理应用中的所有样式.

    提供各种UI组件的样式定义和动态样式生成方法。
    """

    # ===== 颜色常量 =====
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
    COLOR_LIGHT_GRAY = "#f5f5f5"
    COLOR_DARK_GRAY = "#333"
    COLOR_WHITE = "#FFFFFF"
    COLOR_DEFAULT_BORDER = "#cccccc"

    # ===== 按钮样式 =====
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

    # ===== 标签样式 =====
    LABEL_STATUS = f"""
        QLabel {{
            font-size: 14pt;
            color: {COLOR_DARK_GRAY};
            padding: 15px;
            border-radius: 5px;
            border: 2px solid #ddd;
            background-color: {COLOR_LIGHT_GRAY};
        }}
    """

    LABEL_TITLE = f"""
        QLabel {{
            font-size: 13pt;
            font-weight: bold;
            color: {COLOR_DARK_GRAY};
            padding: 5px;
        }}
    """

    LABEL_VALUE = """
        QLabel {
            font-size: 12pt;
            padding: 5px;
            border: 1px solid #ddd;
            background-color: white;
            border-radius: 3px;
        }
    """

    # ===== 输入框样式 =====
    LINE_EDIT = """
        QLineEdit {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 11pt;
            background-color: white;
        }
        QLineEdit:focus {
            border-color: #2196F3;
        }
        QLineEdit:disabled {
            background-color: #f5f5f5;
            color: #999;
        }
    """

    SPIN_BOX = """
        QSpinBox {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 11pt;
            background-color: white;
        }
        QSpinBox:focus {
            border-color: #2196F3;
        }
        QSpinBox:disabled {
            background-color: #f5f5f5;
            color: #999;
        }
    """

    # ===== 组框样式 =====
    GROUP_BOX = f"""
        QGroupBox {{
            font-size: 12pt;
            font-weight: bold;
            border: 2px solid {COLOR_PRIMARY};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            color: {COLOR_PRIMARY};
        }}
    """

    # ===== 进度条样式 =====
    PROGRESS_BAR = f"""
        QProgressBar {{
            border: 2px solid {COLOR_PRIMARY};
            border-radius: 5px;
            text-align: center;
            font-size: 11pt;
            font-weight: bold;
        }}
        QProgressBar::chunk {{
            background-color: {COLOR_PRIMARY};
        }}
    """

    # ===== 传感器测试样式 =====
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

    # ===== 表格样式 =====
    TABLE_WIDGET = """
        QTableWidget {
            border: 1px solid #ddd;
            gridline-color: #ddd;
            background-color: white;
            font-size: 10pt;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #2196F3;
            color: white;
        }
        QHeaderView::section {
            background-color: #f5f5f5;
            padding: 8px;
            border: 1px solid #ddd;
            font-weight: bold;
        }
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
        logger.trace(f"")
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
        logger.trace(f"")
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
