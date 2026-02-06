"""HansLoguru 使用示例模块.

演示如何使用多文件、多级别日志配置功能。
"""

from hans_loguru import HansLoguru, LogFileConfig
from loguru import logger
import multiprocessing
import datetime
from multiprocessing import freeze_support


def worker_process(processing_queue: multiprocessing.Queue, worker_id: int):
    """子进程工作函数示例.

    演示在子进程中配置和使用HansLoguru日志系统。

    :param processing_queue: 日志消息队列
    :type processing_queue: multiprocessing.Queue
    :param worker_id: 工作进程ID
    :type worker_id: int

    .. note:: 每个子进程必须重新配置logger
    """
    # 每个子进程必须重新配置 logger
    # console_output=True 表示在子进程中也输出到终端
    # console_level="INFO" 表示子进程终端只显示 INFO 及以上级别
    HansLoguru.add(
        processing_queue,
        level="TRACE",
        console_output=True,    # 启用子进程终端输出
        console_level="INFO"    # 子进程终端输出级别
    )

    logger.info(f"子进程 {worker_id} 开始执行")
    logger.trace("这是 TRACE 级别日志 - 只会在 all.log 中")
    logger.debug("这是 DEBUG 级别日志 - 只会在 all.log 中")
    logger.info("这是 INFO 级别日志 - 会在 all.log 和 info.log 中，也会显示在终端")
    logger.success("这是 SUCCESS 级别日志")
    logger.warning("这是 WARNING 级别日志")
    logger.error("这是 ERROR 级别日志 - 会在所有文件中")
    logger.critical("这是 CRITICAL 级别日志 - 会在所有文件中")
    logger.info(f"子进程 {worker_id} 执行完成")


if __name__ == "__main__":
    freeze_support()

    # 获取当前时间作为日志文件名的一部分
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # ========== 示例1: 基本使用 - 配置多个日志文件 ==========
    log_files = [
        # 记录所有级别的日志（TRACE及以上）
        LogFileConfig(
            file_path=f"./logs/{current_time}_all.log",
            level="TRACE",
            rotation="10 MB",      # 文件大小达到10MB时自动轮转
            retention="7 days",    # 保留最近7天的日志
            compression="zip"      # 旧日志压缩为zip格式
        ),

        # 只记录 INFO 及以上级别的日志
        LogFileConfig(
            file_path=f"./logs/{current_time}_info.log",
            level="INFO"
        ),

        # 只记录 ERROR 及以上级别的日志
        LogFileConfig(
            file_path=f"./logs/{current_time}_error.log",
            level="ERROR",
            retention="30 days"    # 错误日志保留30天
        ),
    ]

    # 启动监听进程
    # console_level="INFO" 表示终端只显示 INFO 及以上级别的日志
    HansLoguru.listener_process_start(log_files=log_files, console_level="INFO")

    # 主进程也需要配置 logger
    HansLoguru.add(HansLoguru.hans_loguru_queue, level="TRACE")

    # ========== 主进程日志测试 ==========
    print("\n========== 主进程日志测试 ==========")
    logger.trace("主进程 TRACE - 只在 all.log 中，不在终端显示")
    logger.debug("主进程 DEBUG - 只在 all.log 中，不在终端显示")
    logger.info("主进程 INFO - 在 all.log 和 info.log 中，终端显示")
    logger.success("主进程 SUCCESS - 在 all.log 和 info.log 中，终端显示")
    logger.warning("主进程 WARNING - 在 all.log 和 info.log 中，终端显示")
    logger.error("主进程 ERROR - 在所有日志文件中，终端显示")
    logger.critical("主进程 CRITICAL - 在所有日志文件中，终端显示")

    # ========== 子进程日志测试 ==========
    print("\n========== 启动子进程测试 ==========")
    processes = []
    for i in range(2):
        p = multiprocessing.Process(
            target=worker_process,
            args=(HansLoguru.hans_loguru_queue, i+1)
        )
        processes.append(p)
        p.start()
        logger.info(f"启动子进程 {i+1}")

    # 等待所有子进程结束
    for p in processes:
        p.join()

    # ========== 结束 ==========
    logger.info("所有子进程已完成")
    HansLoguru.listener_process_stop()
    logger.info("主进程结束")

    print("\n========== 日志文件说明 ==========")
    print(f"1. {current_time}_all.log - 包含所有级别的日志 (TRACE及以上)")
    print(f"2. {current_time}_info.log - 只包含 INFO 及以上级别的日志")
    print(f"3. {current_time}_error.log - 只包含 ERROR 及以上级别的日志")
    print(f"4. 终端输出 - 只显示 INFO 及以上级别的日志")
    print("\n请查看 ./logs/ 目录下的日志文件以验证配置")

    input("\n按任意键退出")
