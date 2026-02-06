from loguru import logger
import sys

# 配置以便查看完整堆栈
logger.remove()
logger.add(
    sys.stderr,
    format="{time:HH:mm:ss} | {level} | {message}\n{exception}",
    level="DEBUG"
)

def function_a():
    function_b()

def function_b():
    try:
        # 模拟一个非致命问题
        import os
        if not os.path.exists("temp.txt"):
            # 创建一个异常来记录堆栈
            raise FileNotFoundError("临时文件不存在")
    except FileNotFoundError as e:
        # 使用 warning 记录堆栈
        logger.opt(exception=e).warning("文件不存在，使用默认值")
        return "default"

def function_c():
    # 无异常时记录堆栈
    import traceback
    stack = "".join(traceback.format_stack())
    logger.warning(f"函数调用路径:\n{stack}")

if __name__ == "__main__":
    print("=== 示例1：warning 记录异常堆栈 ===")
    function_a()
    
    print("\n=== 示例2：warning 记录调用堆栈 ===")
    function_c()
    
    print("\n=== 示例3：不同级别对比 ===")
    try:
        1 / 0
    except Exception as e:
        logger.debug("debug 级别", exc_info=e)
        logger.info("info 级别", exc_info=e)
        logger.warning("warning 级别", exc_info=e)  # 推荐用于非致命错误
        logger.error("error 级别", exc_info=e)
        logger.critical("critical 级别", exc_info=e)