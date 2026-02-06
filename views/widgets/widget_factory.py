"""UI组件工厂 - 提供标准化的组件创建方法.

此模块提供工厂类用于创建标准化的UI组件。
"""

from PySide6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QSpinBox,
    QGroupBox, QProgressBar, QTableWidget, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from views.styles import AppStyles

from loguru import logger


class WidgetFactory:
    """UI组件工厂类 - 创建标准化的UI组件.

    提供静态方法用于创建各种标准化的UI组件。
    """

    # ===== 按钮创建 =====
    @staticmethod
    def create_start_button(text: str = "开始") -> QPushButton:
        """创建启动按钮.

        :param text: 按钮文本
        :type text: str
        :return: 配置好的启动按钮
        :rtype: QPushButton
        """
        button = QPushButton(text)
        button.setStyleSheet(AppStyles.BUTTON_START)
        return button

    @staticmethod
    def create_stop_button(text: str = "停止") -> QPushButton:
        """创建停止按钮.

        :param text: 按钮文本
        :type text: str
        :return: 配置好的停止按钮
        :rtype: QPushButton
        """
        button = QPushButton(text)
        button.setStyleSheet(AppStyles.BUTTON_STOP)
        return button

    @staticmethod
    def create_normal_button(text: str) -> QPushButton:
        """创建普通按钮.

        :param text: 按钮文本
        :type text: str
        :return: 配置好的普通按钮
        :rtype: QPushButton
        """
        button = QPushButton(text)
        button.setStyleSheet(AppStyles.BUTTON_NORMAL)
        return button

    @staticmethod
    def create_custom_button(text: str, bg_color: str, hover_color: str = None, pressed_color: str = None) -> QPushButton:
        """创建自定义颜色的按钮.

        :param text: 按钮文本
        :type text: str
        :param bg_color: 背景颜色
        :type bg_color: str
        :param hover_color: 悬停颜色
        :type hover_color: str, optional
        :param pressed_color: 按下颜色
        :type pressed_color: str, optional
        :return: 配置好的自定义按钮
        :rtype: QPushButton
        """
        button = QPushButton(text)
        button.setStyleSheet(AppStyles.get_button_style(bg_color, hover_color, pressed_color))
        return button

    # ===== 标签创建 =====
    @staticmethod
    def create_status_label(text: str = "", bg_color: str = "#f5f5f5", border_color: str = None) -> QLabel:
        """创建状态标签.

        :param text: 标签文本
        :type text: str
        :param bg_color: 背景颜色
        :type bg_color: str
        :param border_color: 边框颜色
        :type border_color: str, optional
        :return: 配置好的状态标签
        :rtype: QLabel
        """
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(AppStyles.get_status_style(bg_color, border_color))
        return label

    @staticmethod
    def create_title_label(text: str) -> QLabel:
        """创建标题标签.

        :param text: 标签文本
        :type text: str
        :return: 配置好的标题标签
        :rtype: QLabel
        """
        label = QLabel(text)
        label.setStyleSheet(AppStyles.LABEL_TITLE)
        return label

    @staticmethod
    def create_value_label(text: str = "") -> QLabel:
        """创建值显示标签.

        :param text: 标签文本
        :type text: str
        :return: 配置好的值显示标签
        :rtype: QLabel
        """
        label = QLabel(text)
        label.setStyleSheet(AppStyles.LABEL_VALUE)
        return label

    # ===== 输入框创建 =====
    @staticmethod
    def create_line_edit(text: str = "", placeholder: str = "") -> QLineEdit:
        """创建文本输入框.

        :param text: 默认文本
        :type text: str
        :param placeholder: 占位符文本
        :type placeholder: str
        :return: 配置好的文本输入框
        :rtype: QLineEdit
        """
        line_edit = QLineEdit(text)
        if placeholder:
            line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet(AppStyles.LINE_EDIT)
        return line_edit

    @staticmethod
    def create_spin_box(min_val: int = 0, max_val: int = 100, default: int = 0) -> QSpinBox:
        """创建数字输入框.

        :param min_val: 最小值
        :type min_val: int
        :param max_val: 最大值
        :type max_val: int
        :param default: 默认值
        :type default: int
        :return: 配置好的数字输入框
        :rtype: QSpinBox
        """
        spin_box = QSpinBox()
        spin_box.setMinimum(min_val)
        spin_box.setMaximum(max_val)
        spin_box.setValue(default)
        spin_box.setStyleSheet(AppStyles.SPIN_BOX)
        return spin_box

    # ===== 组框创建 =====
    @staticmethod
    def create_group_box(title: str) -> QGroupBox:
        """创建组框.

        :param title: 组框标题
        :type title: str
        :return: 配置好的组框
        :rtype: QGroupBox
        """
        group_box = QGroupBox(title)
        group_box.setStyleSheet(AppStyles.GROUP_BOX)
        return group_box

    # ===== 进度条创建 =====
    @staticmethod
    def create_progress_bar(min_val: int = 0, max_val: int = 100) -> QProgressBar:
        """创建进度条.

        :param min_val: 最小值
        :type min_val: int
        :param max_val: 最大值
        :type max_val: int
        :return: 配置好的进度条
        :rtype: QProgressBar
        """
        progress_bar = QProgressBar()
        progress_bar.setMinimum(min_val)
        progress_bar.setMaximum(max_val)
        progress_bar.setValue(0)
        progress_bar.setStyleSheet(AppStyles.PROGRESS_BAR)
        return progress_bar

    # ===== 表格创建 =====
    @staticmethod
    def create_table_widget(rows: int = 0, columns: int = 0) -> QTableWidget:
        """创建表格组件.

        :param rows: 行数
        :type rows: int
        :param columns: 列数
        :type columns: int
        :return: 配置好的表格组件
        :rtype: QTableWidget
        """
        table = QTableWidget(rows, columns)
        table.setStyleSheet(AppStyles.TABLE_WIDGET)
        return table

    # ===== 布局创建 =====
    @staticmethod
    def create_vbox_layout(spacing: int = 10, margins: tuple = (10, 10, 10, 10)) -> QVBoxLayout:
        """创建垂直布局.

        :param spacing: 组件间距
        :type spacing: int
        :param margins: 边距 (left, top, right, bottom)
        :type margins: tuple
        :return: 配置好的垂直布局
        :rtype: QVBoxLayout
        """
        layout = QVBoxLayout()
        layout.setSpacing(spacing)
        layout.setContentsMargins(*margins)
        return layout

    @staticmethod
    def create_hbox_layout(spacing: int = 10, margins: tuple = (0, 0, 0, 0)) -> QHBoxLayout:
        """创建水平布局.

        :param spacing: 组件间距
        :type spacing: int
        :param margins: 边距 (left, top, right, bottom)
        :type margins: tuple
        :return: 配置好的水平布局
        :rtype: QHBoxLayout
        """
        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        layout.setContentsMargins(*margins)
        return layout


class LabeledInput:
    """标签+输入框组合.

    提供创建带标签的输入组件的静态方法。
    """

    @staticmethod
    def create_labeled_line_edit(label_text: str, default_value: str = "", placeholder: str = "") -> tuple:
        """创建带标签的文本输入框.

        :param label_text: 标签文本
        :type label_text: str
        :param default_value: 默认值
        :type default_value: str
        :param placeholder: 占位符
        :type placeholder: str
        :return: (标签, 输入框)元组
        :rtype: tuple
        """
        label = WidgetFactory.create_title_label(label_text)
        line_edit = WidgetFactory.create_line_edit(default_value, placeholder)
        return label, line_edit

    @staticmethod
    def create_labeled_spin_box(label_text: str, min_val: int = 0, max_val: int = 100, default: int = 0) -> tuple:
        """创建带标签的数字输入框.

        :param label_text: 标签文本
        :type label_text: str
        :param min_val: 最小值
        :type min_val: int
        :param max_val: 最大值
        :type max_val: int
        :param default: 默认值
        :type default: int
        :return: (标签, 数字输入框)元组
        :rtype: tuple
        """
        label = WidgetFactory.create_title_label(label_text)
        spin_box = WidgetFactory.create_spin_box(min_val, max_val, default)
        return label, spin_box

    @staticmethod
    def create_labeled_value(label_text: str, value_text: str = "") -> tuple:
        """创建标签+值显示组合.

        :param label_text: 标签文本
        :type label_text: str
        :param value_text: 值文本
        :type value_text: str
        :return: (标签, 值标签)元组
        :rtype: tuple
        """
        label = WidgetFactory.create_title_label(label_text)
        value_label = WidgetFactory.create_value_label(value_text)
        return label, value_label
