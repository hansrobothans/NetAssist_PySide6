"""HansLoguru - 支持多进程的日志记录工具.

主要功能：
    - 支持多进程日志记录，自动收集所有子进程的日志
    - 支持配置多个日志文件，每个文件可设置不同的日志级别
    - 支持独立设置终端输出的日志级别
    - 支持日志轮转、保留期限和压缩功能

使用示例::

    from hans_loguru import HansLoguru, LogFileConfig, ConsoleConfig
    from loguru import logger

    # 配置多个日志文件
    log_files = [
        LogFileConfig("./logs/all.log", level="TRACE", rotation="10 MB"),
        LogFileConfig("./logs/info.log", level="INFO"),
        LogFileConfig("./logs/error.log", level="ERROR", retention="30 days"),
    ]

    # 配置控制台输出
    console_config = ConsoleConfig(enabled=True, level="INFO", colorize=True)

    # 启动监听进程
    HansLoguru.listener_process_start(log_files=log_files, console_config=console_config)
    HansLoguru.add(HansLoguru.hans_loguru_queue)

    # 使用logger
    logger.info("这条日志会输出到终端和所有INFO及以上级别的文件")
    logger.debug("这条只会输出到all.log文件，不会显示在终端")

    # 结束时停止监听
    HansLoguru.listener_process_stop()
"""

from loguru import logger
import multiprocessing
import threading
import datetime
import time
import sys
import pickle
import os
from multiprocessing import freeze_support
from typing import List, Optional

class ConsoleConfig:
    """控制台日志配置类.

    用于配置控制台日志输出的参数。
    """

    def __init__(self, enabled: bool = True, level: str = "TRACE",
                 format: Optional[str] = None, colorize: bool = True):
        """初始化控制台日志配置.

        :param enabled: 是否启用控制台输出
        :type enabled: bool
        :param level: 日志级别 (TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL)
        :type level: str
        :param format: 日志格式字符串，如 None 则使用默认格式
        :type format: Optional[str]
        :param colorize: 是否使用颜色
        :type colorize: bool
        """
        self.enabled = enabled
        self.level = level.upper() if level else "TRACE"
        self.format = format
        self.colorize = colorize


class LogFileConfig:
    """日志文件配置类.

    用于配置单个日志文件的参数。
    """

    def __init__(self, file_path: str, level: str = "TRACE", rotation: Optional[str] = None,
                 retention: Optional[str] = None, compression: Optional[str] = None,
                 format: Optional[str] = None):
        """初始化日志文件配置.

        :param file_path: 日志文件路径
        :type file_path: str
        :param level: 日志级别 (TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL)
        :type level: str
        :param rotation: 日志轮转规则，如 "500 MB", "12:00", "1 week"
        :type rotation: Optional[str]
        :param retention: 日志保留规则，如 "10 days", "20"
        :type retention: Optional[str]
        :param compression: 压缩格式，如 "zip", "tar.gz"
        :type compression: Optional[str]
        :param format: 日志格式字符串，如 None 则使用默认格式
        :type format: Optional[str]
        """
        self.file_path = file_path
        self.level = level.upper()
        self.rotation = rotation
        self.retention = retention
        self.compression = compression
        self.format = format

class HansLoguru():
    """多进程日志记录核心类.

    提供多进程环境下的日志收集和处理功能。
    """

    # 定义一个队列,用于存储日志信息
    hans_loguru_queue = multiprocessing.Queue()
    # 定义一个监听器,用于监听日志信息
    listener = None

    def __init__(self):
        """初始化HansLoguru实例."""
        pass

    def log_with_context(self, level, message):
        """打印带有上下文信息的日志.

        包含调用者所在行号、函数名等信息。

        :param level: 日志级别
        :type level: str
        :param message: 日志消息
        :type message: str

        .. todo:: 实现此方法的具体功能
        """
        pass
    
    @classmethod
    def add(cls, processing_queue: multiprocessing.Queue, level="TRACE",
            console_output: bool = False, console_level: str = "TRACE"):
        """子进程初始化logger方法.

        每个子进程创建时，需使用此方法初始化logger。

        :param processing_queue: 传送消息的队列
        :type processing_queue: multiprocessing.Queue
        :param level: 日志消息传送到队列的最低级别
        :type level: str
        :param console_output: 是否在子进程中也输出到终端
        :type console_output: bool
        :param console_level: 子进程终端输出的日志级别
        :type console_level: str
        """
        logger.remove()

        # 添加队列处理器 - 传递完整的记录信息
        def queue_sink(msg):
            # 处理异常信息
            exception_str = None
            if msg.record["exception"] is not None:
                exc_type, exc_value, exc_tb = msg.record["exception"]
                if exc_type is not None:
                    import traceback
                    exception_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))

            log_data = {
                "type": "worker",
                "message": msg.record["message"],
                "level": msg.record["level"].name,
                "process": os.getpid(),
                "thread": threading.current_thread().ident,
                "time": msg.record["time"].isoformat(),
                "file": msg.record["file"].name,
                "line": msg.record["line"],
                "function": msg.record["function"],
                "name": msg.record["name"],
                "exception": exception_str
            }
            processing_queue.put(log_data)

        logger.add(queue_sink, level=level)

        # 如果启用了子进程终端输出
        if console_output and sys.stderr is not None:
            # 定义子进程终端输出格式
            process_id = os.getpid()
            thread_id = threading.current_thread().ident
            subprocess_fmt = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                f"<cyan>P{process_id}</cyan>/<magenta>T{thread_id}</magenta> | "
                "<cyan>{file.name}</cyan> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            )
            logger.add(
                sys.stderr,
                format=subprocess_fmt,
                level=console_level.upper()
            )

    @classmethod
    def add_init(cls, log_files: Optional[List[LogFileConfig]] = None,
                 console_config: Optional[ConsoleConfig] = None):
        """监听进程初始化.

        设置日志格式和输出目标。

        :param log_files: 日志文件配置列表
        :type log_files: Optional[List[LogFileConfig]]
        :param console_config: 控制台日志配置对象
        :type console_config: Optional[ConsoleConfig]
        :return: 日志处理器（监听进程专用的logger）
        """
        # 解析控制台配置
        if console_config is None:
            console_config = ConsoleConfig()

        console_enabled = console_config.enabled
        console_level = console_config.level
        console_format = console_config.format

        # 监听进程自身日志配置
        listener_logger = logger.bind(is_listener=True)
        listener_logger.remove()
        thread_id = threading.current_thread().ident
        process_id = os.getpid()
        listener_fmt = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                # "LISTENER | "
                f"<cyan>P{process_id}</cyan>/<magenta>T{thread_id}</magenta> | "
                "<cyan>{file}</cyan> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            )

        # 修复: 检查 sys.stderr 是否可用
        # 在 PyInstaller 打包的 --windowed 模式下, sys.stderr 可能为 None
        if console_enabled and sys.stderr is not None:
            listener_logger.add(
                sys.stderr,
                format=listener_fmt,
                level=console_level.upper(),
                filter=lambda record: "is_listener" in record["extra"]
            )

        # 注意：监听进程自身的日志不写入文件，避免与工作进程日志文件冲突
        # 监听进程只负责转发来自队列的日志到文件，自己的内部日志只输出到控制台

        # 工作进程日志的控制台格式
        # 如果配置了format，使用配置的格式；否则使用默认格式
        if console_format:
            # 配置的格式需要适配extra字段
            # 将配置中的占位符转换为extra字段访问
            worker_fmt = console_format
        else:
            # 默认格式
            worker_fmt = (
                    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                    "<level>{level: <8}</level> | "
                    "<cyan>P{extra[process]}</cyan>/<magenta>T{extra[thread]}</magenta> | "
                    "<cyan>{extra[file]}</cyan> | "
                    "<cyan>{extra[name]}</cyan>:<cyan>{extra[function]}</cyan>:<cyan>{extra[line]}</cyan> - "
                    "<level>{message}</level>"
                )

        # 工作进程日志处理器配置 - 终端输出
        # 修复: 检查 sys.stderr 是否可用
        if console_enabled and sys.stderr is not None:
            logger.add(
                sys.stderr,
                format=worker_fmt,
                level=console_level.upper(),
                filter=lambda record: "is_listener" not in record["extra"]
            )

        # 工作进程日志处理器配置 - 文件输出
        if log_files:
            for log_config in log_files:
                # 确保日志目录存在
                log_dir = os.path.dirname(log_config.file_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)

                # 使用配置的格式，如果没有配置则使用默认格式
                # 注意：配置中的格式需要使用 extra 字段来访问进程/线程信息
                file_format = log_config.format if log_config.format else worker_fmt

                add_kwargs = {
                    "sink": log_config.file_path,
                    "format": file_format,
                    "level": log_config.level,
                    "filter": lambda record: "is_listener" not in record["extra"]
                }

                # 添加可选参数
                if log_config.rotation:
                    add_kwargs["rotation"] = log_config.rotation
                if log_config.retention:
                    add_kwargs["retention"] = log_config.retention
                if log_config.compression:
                    add_kwargs["compression"] = log_config.compression

                logger.add(**add_kwargs)

        return listener_logger

    @classmethod
    def listener_process(cls, processing_queue: multiprocessing.Queue,
                        log_files: Optional[List[LogFileConfig]] = None,
                        console_config: Optional[ConsoleConfig] = None):
        """日志监听进程函数.

        用于接受所有进程的日志信息，并进行汇总处理。

        :param processing_queue: 接收日志信息的队列
        :type processing_queue: multiprocessing.Queue
        :param log_files: 日志文件配置列表
        :type log_files: Optional[List[LogFileConfig]]
        :param console_config: 控制台日志配置对象
        :type console_config: Optional[ConsoleConfig]
        """
        # 自定义格式,显示原始进程和线程信息
        cls.listener_logger = cls.add_init(log_files, console_config)
        
        while True:
            try:
                message = processing_queue.get()
                if message is None:
                    cls.listener_logger.info("收到终止信号,监听进程即将退出")
                    break
                    
                if message["type"] == "worker":
                    # 构建日志消息，如果有异常信息则附加
                    log_message = message["message"]
                    if message.get("exception"):
                        log_message = f"{log_message}\n{message['exception']}"

                    logger.bind(
                        process=message["process"],
                        thread=message["thread"],
                        file=message["file"],
                        line=message["line"],
                        function=message["function"],
                        name=message["name"],  # 绑定name字段
                        time=message["time"]
                    ).log(message["level"], log_message)
            except Exception as e:
                cls.listener_logger.error(f"处理日志时出错: {e}")

    @classmethod
    def listener_process_start(cls, log_files: Optional[List[LogFileConfig]] = None,
                               console_config: Optional[ConsoleConfig] = None) -> multiprocessing.Queue:
        """开启监听进程.

        用于汇总所有监听信息进行处理。

        :param log_files: 日志文件配置列表
        :type log_files: Optional[List[LogFileConfig]]
        :param console_config: 控制台日志配置对象
        :type console_config: Optional[ConsoleConfig]
        :return: 用于接受日志信息的队列
        :rtype: multiprocessing.Queue
        """
        cls.listener = multiprocessing.Process(
            target=HansLoguru.listener_process,
            args=(cls.hans_loguru_queue, log_files, console_config)
        )
        cls.listener.start()
        return cls.hans_loguru_queue

    @classmethod
    def listener_process_stop(cls):
        """停止监听进程.

        发送终止信号并等待进程结束。
        """
        cls.hans_loguru_queue.put(None)
        cls.listener.join() 

class MyClass():
    """测试用例类.

    用于演示多进程和多线程环境下的日志记录。
    """

    def __init__(self):
        """初始化测试类实例."""
        pass

    def worker_thread(self):
        """工作线程函数.

        演示线程中的日志记录。
        """
        # 线程不需要修改格式
        logger.info("子线程开始")
        time.sleep(1)
        logger.info("子线程结束")
        time.sleep(1)

    def worker_process(self, processing_queue: multiprocessing.Queue):
        """工作进程函数.

        演示子进程中的日志记录配置和使用。

        :param processing_queue: 日志消息队列
        :type processing_queue: multiprocessing.Queue
        """
        # HANS: B 每个子进程必须重新配置 logger
        HansLoguru.add(processing_queue)
        # HANS: E 主进程配置 logger

        # logger.trace("子进程开始")
        # logger.debug("子进程开始")
        # logger.info("子进程开始")
        # logger.warning("子进程开始")
        # logger.info("子进程开始")
        # logger.success("子进程开始")
        # logger.warning("子进程开始")
        # logger.error("子进程开始")
        # logger.critical("子进程开始")
        # logger.exception("子进程开始")
        if False:
            # 启动 3 个子进程
            threads = []
            for _ in range(1):
                t = threading.Thread(target=self.worker_thread)
                threads.append(t)
                t.start()
            time.sleep(1)
            # for _ in range(10000):
            #     logger.info("子进程运行中")

        logger.trace("子进程结束")
        logger.debug("子进程结束")
        logger.info("子进程结束")
        logger.warning("子进程结束")
        logger.info("子进程结束")
        logger.success("子进程结束")
        logger.warning("子进程结束")
        logger.error("子进程结束")
        logger.critical("子进程结束")
        logger.exception("子进程结束")
        time.sleep(0.1)

    def example_function(self):
        """示例函数.

        创建并启动多个子进程，演示多进程日志收集。
        """
        # logger.info("主进程开始")
        # logger.trace("TRACE")
        # logger.debug("DEBUG")
        # logger.info("INFO")
        # logger.success("SUCCESS")
        # logger.warning("WARNING")
        # logger.error("ERROR")
        # logger.critical("CRITICAL")

        # 启动 3 个子进程
        processes = []
        for _ in range(2):
            p = multiprocessing.Process(target=self.worker_process, args=(HansLoguru.hans_loguru_queue,))
            processes.append(p)
            p.start()

        # 等待所有子进程结束
        for p in processes:
            p.join()
        
if __name__ == "__main__":
    freeze_support()
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # 配置多个日志文件，每个文件可以有不同的日志级别
    log_files = [
        # 所有级别的日志（TRACE及以上）
        LogFileConfig(
            file_path=f"./logs/{current_time}_all.log",
            level="TRACE",
            rotation="10 MB",  # 每10MB轮转一次
            retention="7 days",  # 保留7天
            compression="zip"  # 压缩为zip格式
        ),
        # 只记录INFO及以上级别的日志
        LogFileConfig(
            file_path=f"./logs/{current_time}_info.log",
            level="INFO"
        ),
        # 只记录ERROR及以上级别的日志
        LogFileConfig(
            file_path=f"./logs/{current_time}_error.log",
            level="ERROR",
            retention="30 days"  # 错误日志保留30天
        ),
    ]

    # HANS: B 主进程配置 logger
    # 配置控制台日志
    console_config = ConsoleConfig(
        enabled=True,
        level="INFO",
        format=None,  # 使用默认格式
        colorize=True
    )
    HansLoguru.listener_process_start(log_files=log_files, console_config=console_config)
    HansLoguru.add(HansLoguru.hans_loguru_queue)
    # HANS: E 主进程配置 logger

    # logger.trace("TRACE")
    # logger.debug("DEBUG")
    # logger.info("INFO")
    # logger.success("SUCCESS")
    # logger.warning("WARNING")
    # logger.error("ERROR")
    # logger.critical("CRITICAL")
    # logger.exception("EXCEPTION")

    # 在保护块内创建实例
    my_class = MyClass()  # 注意变量名不要和类名相同
    my_class.example_function()

    logger.trace("TRACE")
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.success("SUCCESS")
    logger.warning("WARNING")
    logger.error("ERROR")
    logger.critical("CRITICAL")
    logger.exception("EXCEPTION")

    # HANS: B 主进程结束 logger
    logger.info("所有子进程已完成")
    HansLoguru.listener_process_stop()
    logger.info("主进程结束")
    # HANS: E 主进程结束 logger
    input("按任意键退出")