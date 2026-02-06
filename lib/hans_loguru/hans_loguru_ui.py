"""HansLoguru UI - 支持UI的日志记录工具.

主要功能：
    - 继承HansLoguru，提供带缓冲区的日志记录
    - 提供可配置的日志缓冲区，用于UI组件显示历史日志
    - 支持多进程环境下的日志收集和缓冲

使用示例（带UI的程序）::

    from hans_loguru import HansLoguruUI, LogFileConfig, ConsoleConfig
    from loguru import logger

    # 配置日志文件
    log_files = [
        LogFileConfig("./logs/all.log", level="TRACE")
    ]

    # 配置控制台
    console_config = ConsoleConfig(
        enabled=True,
        level="INFO",
        format=None,  # 使用默认格式
        colorize=True
    )

    # 使用 HansLoguruUI 启动（带缓冲区）
    HansLoguruUI.listener_process_start(
        log_files=log_files,
        console_config=console_config,
        buffer_size=2000  # 缓冲区大小
    )
    HansLoguruUI.add(HansLoguruUI.hans_loguru_queue)

    # UI组件可以通过 HansLoguruUI.get_log_buffer() 获取历史日志

使用示例（不带UI的程序）::

    from hans_loguru import HansLoguru, LogFileConfig, ConsoleConfig
    from loguru import logger

    # 配置日志文件
    log_files = [LogFileConfig("./logs/all.log", level="TRACE")]

    # 配置控制台
    console_config = ConsoleConfig(enabled=True, level="INFO")

    # 使用基础 HansLoguru（无缓冲区开销）
    HansLoguru.listener_process_start(log_files=log_files, console_config=console_config)
    HansLoguru.add(HansLoguru.hans_loguru_queue)
"""

from loguru import logger
import multiprocessing
import threading
import os
from typing import Optional, List
from collections import deque
from .hans_loguru import HansLoguru, LogFileConfig, ConsoleConfig


class HansLoguruUI(HansLoguru):
    """支持UI的日志记录类.

    继承HansLoguru，添加日志缓冲区功能，用于支持UI组件显示历史日志。

    主要特性：
        - 提供可配置大小的日志缓冲区
        - 线程安全的缓冲区操作
        - 自动收集所有日志到缓冲区
    """

    # 日志缓冲区，用于存储历史日志（供UI组件使用）
    log_buffer = deque(maxlen=1000)  # 默认保存1000条日志
    # 日志缓冲区锁
    log_buffer_lock = threading.Lock()

    @classmethod
    def get_log_buffer(cls):
        """获取日志缓冲区的副本.

        用于UI组件加载历史日志。

        :return: 日志记录列表
        :rtype: list
        """
        with cls.log_buffer_lock:
            return list(cls.log_buffer)

    @classmethod
    def clear_log_buffer(cls):
        """清空日志缓冲区."""
        with cls.log_buffer_lock:
            cls.log_buffer.clear()

    @classmethod
    def set_buffer_size(cls, maxlen: int):
        """设置日志缓冲区大小.

        :param maxlen: 最大日志条数
        :type maxlen: int
        """
        with cls.log_buffer_lock:
            # 保存现有日志
            existing_logs = list(cls.log_buffer)
            # 创建新的缓冲区
            cls.log_buffer = deque(existing_logs, maxlen=maxlen)

    @classmethod
    def add(cls, processing_queue: multiprocessing.Queue, level="TRACE",
            console_output: bool = False, console_level: str = "TRACE",
            enable_buffer: bool = True):
        """子进程初始化logger方法.

        每个子进程创建时，需使用此方法初始化logger。重写父类方法，添加缓冲区支持。

        :param processing_queue: 传送消息的队列
        :type processing_queue: multiprocessing.Queue
        :param level: 日志消息传送到队列的最低级别
        :type level: str
        :param console_output: 是否在子进程中也输出到终端
        :type console_output: bool
        :param console_level: 子进程终端输出的日志级别
        :type console_level: str
        :param enable_buffer: 是否启用日志缓冲（用于UI显示历史日志）
        :type enable_buffer: bool
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

            # 添加到缓冲区（用于UI显示）
            if enable_buffer:
                with cls.log_buffer_lock:
                    cls.log_buffer.append(log_data)

        logger.add(queue_sink, level=level)

        # 如果启用了子进程终端输出，调用父类的实现
        if console_output:
            import sys
            if sys.stderr is not None:
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
    def listener_process(cls, processing_queue: multiprocessing.Queue,
                        log_files: Optional[List[LogFileConfig]] = None,
                        console_config: Optional['ConsoleConfig'] = None,
                        buffer_size: int = 1000):
        """日志监听进程函数.

        用于接受所有进程的日志信息，并进行汇总处理。重写父类方法，添加缓冲区支持。

        :param processing_queue: 接收日志信息的队列
        :type processing_queue: multiprocessing.Queue
        :param log_files: 日志文件配置列表
        :type log_files: Optional[List[LogFileConfig]]
        :param console_config: 控制台日志配置对象
        :type console_config: Optional[ConsoleConfig]
        :param buffer_size: 日志缓冲区大小
        :type buffer_size: int
        """
        # 设置缓冲区大小
        cls.set_buffer_size(buffer_size)

        # 调用父类的 add_init
        cls.listener_logger = cls.add_init(log_files, console_config)

        while True:
            try:
                message = processing_queue.get()
                if message is None:
                    cls.listener_logger.info("收到终止信号，监听进程即将退出")
                    break

                if message["type"] == "worker":
                    # 添加到缓冲区
                    with cls.log_buffer_lock:
                        cls.log_buffer.append(message)

                    # 构建日志消息，如果有异常信息则附加
                    log_message = message["message"]
                    if message.get("exception"):
                        log_message = f"{log_message}\n{message['exception']}"

                    # 记录日志
                    logger.bind(
                        process=message["process"],
                        thread=message["thread"],
                        file=message["file"],
                        line=message["line"],
                        function=message["function"],
                        name=message["name"],
                        time=message["time"]
                    ).log(message["level"], log_message)
            except Exception as e:
                cls.listener_logger.error(f"处理日志时出错: {e}")

    @classmethod
    def listener_process_start(cls, log_files: Optional[List[LogFileConfig]] = None,
                               console_config: Optional['ConsoleConfig'] = None,
                               buffer_size: int = 1000) -> multiprocessing.Queue:
        """开启监听进程.

        用于汇总所有监听信息进行处理。重写父类方法，添加缓冲区大小参数。

        :param log_files: 日志文件配置列表
        :type log_files: Optional[List[LogFileConfig]]
        :param console_config: 控制台日志配置对象
        :type console_config: Optional[ConsoleConfig]
        :param buffer_size: 日志缓冲区大小
        :type buffer_size: int
        :return: 用于接受日志信息的队列
        :rtype: multiprocessing.Queue
        """
        cls.listener = multiprocessing.Process(
            target=cls.listener_process,
            args=(cls.hans_loguru_queue, log_files, console_config, buffer_size)
        )
        cls.listener.start()
        return cls.hans_loguru_queue
