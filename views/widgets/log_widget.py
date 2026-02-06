"""LogWidget - 可移植的GUI日志显示组件.

主要功能:
    - 提供独立的LogWidget组件，可在任何PySide6/PyQt6项目中使用
    - 自动集成loguru日志系统
    - 支持彩色日志显示、日志级别过滤、清空等功能
    - 线程安全，支持多线程/多进程环境
    - 支持从 HansLoguruUI 缓冲区加载历史日志

使用示例::

    from PySide6.QtWidgets import QApplication, QMainWindow
    from ui.widgets.log_widget import LogWidget
    from loguru import logger

    app = QApplication([])
    window = QMainWindow()

    # 创建日志组件
    log_widget = LogWidget()
    window.setCentralWidget(log_widget)
    window.show()

    # 使用logger，日志会自动显示在GUI中
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")

    app.exec()
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QObject, Slot
from PySide6.QtGui import QTextCharFormat, QColor, QFont
from loguru import logger
from typing import Optional, Dict
import os
import threading
from datetime import datetime


class LogSignals(QObject):
    """日志信号类 - 用于线程安全的日志传递.

    提供信号用于在线程间传递日志消息。
    """
    log_message = Signal(str, str)  # message, level


class LogWidget(QWidget):
    """可移植的日志显示组件.

    功能:
        - 实时显示loguru日志
        - 彩色显示不同级别的日志
        - 日志级别过滤
        - 清空日志
        - 自动滚动
        - 可选择是否显示时间戳、进程/线程信息等
        - 从 HansLoguruUI 加载历史日志
    """

    # 日志级别对应的颜色（可自定义）
    DEFAULT_LEVEL_COLORS = {
        "TRACE": "#9E9E9E",      # 灰色
        "DEBUG": "#2196F3",      # 蓝色
        "INFO": "#4CAF50",       # 绿色
        "SUCCESS": "#00C853",    # 深绿色
        "WARNING": "#FF9800",    # 橙色
        "ERROR": "#F44336",      # 红色
        "CRITICAL": "#D32F2F",   # 深红色
    }

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        level_colors: Optional[Dict[str, str]] = None,
        log_format: Optional[str] = None,
        default_filter_level: str = "TRACE",
        auto_register: bool = True,
        dark_theme: bool = True,
        load_history: bool = True
    ):
        """初始化日志显示组件.

        :param parent: 父组件
        :type parent: QWidget, optional
        :param level_colors: 自定义日志级别颜色字典
        :type level_colors: Dict[str, str], optional
        :param log_format: 日志格式字符串
        :type log_format: str, optional
        :param default_filter_level: 默认过滤级别
        :type default_filter_level: str
        :param auto_register: 是否自动注册到loguru
        :type auto_register: bool
        :param dark_theme: 是否使用深色主题
        :type dark_theme: bool
        :param load_history: 是否加载历史日志
        :type load_history: bool
        """
        super().__init__(parent)

        # 日志级别颜色
        self.level_colors = level_colors or self.DEFAULT_LEVEL_COLORS
        thread_id = threading.current_thread().ident
        process_id = os.getpid()
        # 日志格式
        if log_format is None:
            self.log_format = (
                    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                    "<level>{level: <8}</level> | "
                    f"<cyan>P{process_id}</cyan>/<magenta>T{thread_id}</magenta> | "
                    "<cyan>{file}</cyan> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                    "<level>{message}</level>"
                )
        else:
            self.log_format = log_format

        # 创建信号对象
        self.signals = LogSignals()
        self.signals.log_message.connect(self._append_log)

        # 日志处理器ID
        self.logger_handler_id = None

        # 当前过滤级别
        self.current_filter_level = default_filter_level

        # 主题设置
        self.dark_theme = dark_theme

        # 保存所有日志记录（用于重新过滤）
        self.all_logs = []

        # 初始化UI
        self.init_ui()

        # 加载历史日志（如果有HansLoguruUI缓冲区）
        if load_history:
            self.load_history_logs()

        # 自动注册到loguru
        if auto_register:
            self.register_logger()

    def init_ui(self):
        """初始化UI.

        创建工具栏和日志显示区域。
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # 工具栏
        toolbar = QHBoxLayout()

        # 清空按钮
        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.clicked.connect(self.clear_logs)
        toolbar.addWidget(self.clear_btn)

        # 日志级别过滤
        toolbar.addWidget(QLabel("显示级别:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"])
        self.level_combo.setCurrentText(self.current_filter_level)
        self.level_combo.currentTextChanged.connect(self.on_level_filter_changed)
        toolbar.addWidget(self.level_combo)

        # 自动滚动选项
        self.auto_scroll_checkbox = QCheckBox("自动滚动")
        self.auto_scroll_checkbox.setChecked(True)
        toolbar.addWidget(self.auto_scroll_checkbox)

        toolbar.addStretch()

        layout.addLayout(toolbar)

        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        # 设置等宽字体
        try:
            # 优先使用 Consolas，如果不存在则使用 Courier New
            self.log_text.setFont(QFont("Consolas", 9))
        except:
            self.log_text.setFont(QFont("Courier New", 9))

        # 应用主题
        if self.dark_theme:
            self.log_text.setStyleSheet("""
                QTextEdit {
                    background-color: #1E1E1E;
                    color: #D4D4D4;
                    border: 1px solid #3C3C3C;
                }
            """)
        else:
            self.log_text.setStyleSheet("""
                QTextEdit {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                }
            """)

        layout.addWidget(self.log_text)

    def load_history_logs(self):
        """从 HansLoguruUI 缓冲区加载历史日志.

        尝试从HansLoguruUI获取历史日志并显示。
        """
        try:
            # 尝试导入 HansLoguruUI
            from lib.hans_loguru.hans_loguru_ui import HansLoguruUI

            # 获取历史日志
            history_logs = HansLoguruUI.get_log_buffer()

            if not history_logs:
                logger.trace("没有找到历史日志")
                return

            logger.trace(f"正在加载 {len(history_logs)} 条历史日志")

            # 逐条显示历史日志
            for log_data in history_logs:
                # 格式化日志消息
                formatted_msg = self._format_log_from_data(log_data)
                level = log_data.get("level", "INFO")

                # 保存到日志列表（用于重新过滤）
                self.all_logs.append({
                    "message": formatted_msg + "\n",
                    "level": level
                })

                # 检查级别过滤
                if not self._should_show_level(level):
                    continue

                # 获取对应级别的颜色
                color = self.level_colors.get(level, "#D4D4D4" if self.dark_theme else "#000000")

                # 设置文本格式
                cursor = self.log_text.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)

                fmt = QTextCharFormat()
                fmt.setForeground(QColor(color))

                # 插入带颜色的文本
                cursor.insertText(formatted_msg + "\n", fmt)

            # 滚动到底部
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.log_text.setTextCursor(cursor)
            self.log_text.ensureCursorVisible()

            logger.trace(f"成功加载 {len(history_logs)} 条历史日志")

        except ImportError:
            logger.trace("HansLoguruUI 不可用，跳过加载历史日志")
        except Exception as e:
            logger.opt(exception=e).warning("加载历史日志失败")

    def _format_log_from_data(self, log_data: dict) -> str:
        """根据日志数据格式化日志消息.

        :param log_data: 日志数据字典
        :type log_data: dict
        :return: 格式化后的日志字符串
        :rtype: str
        """
        try:
            time_str = log_data.get("time", "")
            level = log_data.get("level", "INFO")
            process = log_data.get("process", "")
            thread = log_data.get("thread", "")
            file = log_data.get("file", "")
            name = log_data.get("name", "")
            function = log_data.get("function", "")
            line = log_data.get("line", "")
            message = log_data.get("message", "")

            # 格式化时间
            if time_str:
                # ISO格式转换为可读格式
                try:
                    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    time_formatted = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                except:
                    time_formatted = time_str
            else:
                time_formatted = ""

            # 构建日志字符串
            log_str = (
                f"{time_formatted} | "
                f"{level: <8} | "
                f"P{process}/T{thread} | "
                f"{file} | "
                f"{name}:{function}:{line} - "
                f"{message}"
            )

            return log_str

        except Exception as e:
            logger.opt(exception=e).warning("格式化日志数据失败")
            return str(log_data)

    def register_logger(self, level: str = "TRACE"):
        """注册到loguru日志系统.

        :param level: 日志级别
        :type level: str
        """
        if self.logger_handler_id is not None:
            logger.warning("日志处理器已注册，跳过重复注册")
            return

        # 添加一个自定义的sink，将日志发送到GUI
        self.logger_handler_id = logger.add(
            self._log_sink,
            format=self.log_format,
            level=level,
            colorize=False
        )

        logger.trace("LogWidget已注册到loguru")

    def unregister_logger(self):
        """从loguru日志系统中注销.

        移除注册的日志处理器。
        """
        if self.logger_handler_id is not None:
            logger.remove(self.logger_handler_id)
            self.logger_handler_id = None
            logger.trace("LogWidget已从loguru注销")

    def _log_sink(self, message):
        """自定义日志接收器.

        :param message: 日志消息对象
        """
        # 提取日志级别
        level = message.record['level'].name

        # 通过信号发送到主线程（线程安全）
        self.signals.log_message.emit(str(message), level)

    @Slot(str, str)
    def _append_log(self, message: str, level: str):
        """追加日志到文本框（线程安全）.

        :param message: 日志消息
        :type message: str
        :param level: 日志级别
        :type level: str
        """
        # 保存到日志列表（用于重新过滤）
        self.all_logs.append({
            "message": message,
            "level": level
        })

        # 检查级别过滤
        if not self._should_show_level(level):
            return

        # 获取对应级别的颜色
        color = self.level_colors.get(level, "#D4D4D4" if self.dark_theme else "#000000")

        # 设置文本格式
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))

        # 插入带颜色的文本
        cursor.insertText(message, fmt)

        # 自动滚动到底部
        if self.auto_scroll_checkbox.isChecked():
            self.log_text.setTextCursor(cursor)
            self.log_text.ensureCursorVisible()

    def _should_show_level(self, level: str) -> bool:
        """判断是否应该显示该级别的日志.

        :param level: 日志级别
        :type level: str
        :return: 是否应该显示
        :rtype: bool
        """
        level_order = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]

        if level not in level_order or self.current_filter_level not in level_order:
            return True

        current_index = level_order.index(self.current_filter_level)
        log_index = level_order.index(level)

        return log_index >= current_index

    def clear_logs(self):
        """清空日志显示.

        清空显示区域和内部日志缓存。
        """
        self.log_text.clear()
        # 同时清空保存的日志列表
        self.all_logs.clear()
        logger.debug("GUI日志显示已清空")

    def on_level_filter_changed(self, level: str):
        """日志级别过滤变化.

        :param level: 新的过滤级别
        :type level: str
        """
        self.current_filter_level = level
        logger.debug(f"GUI日志显示级别已设置为: {level}")
        # 重新渲染所有日志
        self._refresh_logs()

    def _refresh_logs(self):
        """重新渲染所有日志（根据当前过滤级别）.

        根据当前过滤级别重新显示所有日志。
        """
        # 清空显示区域
        self.log_text.clear()

        # 重新显示符合条件的日志
        for log_entry in self.all_logs:
            message = log_entry["message"]
            level = log_entry["level"]

            # 检查级别过滤
            if not self._should_show_level(level):
                continue

            # 获取对应级别的颜色
            color = self.level_colors.get(level, "#D4D4D4" if self.dark_theme else "#000000")

            # 设置文本格式
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)

            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))

            # 插入带颜色的文本
            cursor.insertText(message, fmt)

        # 滚动到底部
        if self.auto_scroll_checkbox.isChecked():
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.log_text.setTextCursor(cursor)
            self.log_text.ensureCursorVisible()

    def set_level_colors(self, colors: Dict[str, str]):
        """设置日志级别颜色.

        :param colors: 颜色字典
        :type colors: Dict[str, str]

        .. note:: 示例: {"INFO": "#00FF00", "ERROR": "#FF0000"}
        """
        self.level_colors.update(colors)

    def set_log_format(self, log_format: str):
        """设置日志格式（需要重新注册才能生效）.

        :param log_format: 日志格式字符串
        :type log_format: str

        .. note:: 修改后会自动重新注册日志处理器
        """
        self.log_format = log_format
        if self.logger_handler_id is not None:
            self.unregister_logger()
            self.register_logger()

    def closeEvent(self, event):
        """关闭事件 - 自动移除日志处理器.

        :param event: 关闭事件对象
        :type event: QCloseEvent
        """
        self.unregister_logger()
        super().closeEvent(event)


# 为了兼容性，提供一个简化的函数式API
def create_log_widget(
    parent: Optional[QWidget] = None,
    **kwargs
) -> LogWidget:
    """创建日志显示组件（工厂函数）.

    :param parent: 父组件
    :type parent: QWidget, optional
    :param kwargs: 传递给LogWidget的其他参数
    :return: LogWidget实例
    :rtype: LogWidget
    """
    return LogWidget(parent=parent, **kwargs)


if __name__ == "__main__":
    """测试代码"""
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow
    import time
    import threading

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("LogWidget 测试")
    window.resize(800, 600)

    # 创建日志组件
    log_widget = LogWidget()
    window.setCentralWidget(log_widget)
    window.show()

    # 测试日志输出
    def test_logging():
        time.sleep(0.5)
        logger.trace("这是TRACE级别的日志")
        time.sleep(0.3)
        logger.debug("这是DEBUG级别的日志")
        time.sleep(0.3)
        logger.info("这是INFO级别的日志")
        time.sleep(0.3)
        logger.success("这是SUCCESS级别的日志")
        time.sleep(0.3)
        logger.warning("这是WARNING级别的日志")
        time.sleep(0.3)
        logger.error("这是ERROR级别的日志")
        time.sleep(0.3)
        logger.critical("这是CRITICAL级别的日志")

    # 在后台线程中测试日志
    thread = threading.Thread(target=test_logging)
    thread.start()

    sys.exit(app.exec())
