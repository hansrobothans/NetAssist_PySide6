# main.py
"""调试助手工具主程序模块.

此模块是调试助手应用的入口点，负责初始化日志系统和主窗口。
"""

import sys
import os
from multiprocessing import freeze_support

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from loguru import logger

from lib.hans_loguru import HansLoguruUI
from views import MainWindow
from services.core import ConfigService
from services import ServiceContainer

def main():
    """应用主函数.

    初始化应用环境，配置日志系统，并启动主窗口。

    日志配置从 configs/config.json 中的 logging 节读取，支持：
    - 多个日志文件，每个文件独立配置级别、轮转策略等
    - 控制台输出配置（级别、颜色、格式）
    - 全局日志级别控制

    使用HansLoguruUI支持UI历史日志显示。
    """

    # 创建配置服务实例（自动加载配置文件，不存在则使用默认配置）
    config_service = ConfigService("./configs/config.json")

    # 获取日志配置
    log_files = config_service.get_log_file_configs()
    console_config = config_service.get_console_config()

    # HANS: B 主进程配置 logger（使用HansLoguruUI支持UI历史日志显示）
    # console_config 从配置文件读取，包含enabled、level、format、colorize等
    # buffer_size 参数控制历史日志缓冲区大小（默认1000条）
    HansLoguruUI.listener_process_start(
        log_files=log_files,
        console_config=console_config,
        buffer_size=2000  # 缓冲区大小可根据需要调整
    )
    HansLoguruUI.add(HansLoguruUI.hans_loguru_queue)
    # HANS: E 主进程配置 logger

    # 创建服务容器（注入配置服务）
    container = ServiceContainer(config=config_service)

    try:
        # 创建Qt应用
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # 设置应用图标
        icon_path = None
        try:
            if hasattr(sys, '_MEIPASS'):
                icon_path = os.path.join(getattr(sys, '_MEIPASS'), 'resources', 'logo', 'window.ico')
            else:
                icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'logo', 'window.ico')

            if os.path.exists(icon_path):
                logger.info(f"已加载应用图标: {icon_path}")
                app.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            logger.opt(exception=e).warning("未找到应用图标文件")

        # 创建主窗口（注入服务容器）
        window = MainWindow(container=container)

        # 为主窗口单独设置图标
        if icon_path and os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))

        window.show()

        # 运行应用
        exit_code = app.exec()

        # 清理资源
        logger.info("应用正常退出，开始清理资源...")
        container.cleanup()

        # 清理日志
        HansLoguruUI.listener_process_stop()

        sys.exit(exit_code)

    except Exception as e:
        logger.opt(exception=e).error("应用异常退出")
        container.cleanup()
        HansLoguruUI.listener_process_stop()
        sys.exit(1)


if __name__ == "__main__":
    freeze_support()
    main()