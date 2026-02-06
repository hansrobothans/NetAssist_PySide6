# HansLoguru - 增强的多进程日志工具

基于 loguru 的多进程日志记录工具，支持灵活的多文件、多级别配置。

## 主要功能

### 1. 多进程日志支持
- 自动收集所有子进程的日志
- 统一格式化输出
- 保留进程ID和线程ID信息

### 2. GUI日志显示组件 ⭐新功能
- **可移植的LogWidget组件** - 可在任何PySide6项目中使用
- **实时日志显示** - 自动显示loguru日志
- **彩色日志** - 不同级别用不同颜色显示
- **历史日志加载** - 自动加载之前的日志记录
- **日志级别过滤** - 可选择只显示特定级别
- **线程安全** - 支持多线程/多进程环境

### 3. 日志缓冲功能 ⭐新功能
- **历史日志缓冲** - 默认保存最近1000条日志
- **UI历史加载** - 创建LogWidget时自动加载历史日志
- **可配置大小** - 根据需要调整缓冲区大小

### 4. 多文件配置
- 支持同时配置多个日志文件
- 每个文件可以设置不同的日志级别
- 例如：同时生成详细日志和错误日志

### 5. 独立的终端输出级别
- 终端输出级别可以独立于文件配置
- 例如：文件记录所有日志，但终端只显示重要信息

### 6. 日志管理功能
- **日志轮转 (rotation)**: 按文件大小、时间自动轮转
- **保留策略 (retention)**: 自动清理过期日志
- **压缩功能 (compression)**: 自动压缩旧日志文件

## 安装依赖

```bash
# 核心依赖
pip install loguru

# GUI组件依赖（可选）
pip install PySide6
```

## 快速开始

### GUI日志显示（新功能）

```python
from PySide6.QtWidgets import QApplication, QMainWindow
from hans_loguru import HansLoguruUI, LogFileConfig
from ui.widgets import LogWidget
from loguru import logger
import datetime

# 配置日志文件
current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
log_files = [
    LogFileConfig(f"./logs/{current_time}_all.log", level="TRACE")
]

# 启动日志系统（使用HansLoguruUI，自动启用缓冲区）
HansLoguruUI.listener_process_start(
    log_files=log_files,
    console_level="INFO",
    buffer_size=2000  # 缓冲区大小（默认1000条）
)
HansLoguruUI.add(HansLoguruUI.hans_loguru_queue)

# 程序启动时产生一些日志
logger.info("应用程序启动")
logger.debug("正在初始化...")

# 创建GUI应用
app = QApplication([])
window = QMainWindow()
window.setWindowTitle("日志查看器")
window.resize(1000, 600)

# 创建日志显示组件（会自动加载之前的日志）
log_widget = LogWidget(
    default_filter_level="TRACE",  # 默认显示所有级别
    auto_register=True,            # 自动注册到loguru
    dark_theme=True,               # 深色主题
    load_history=True              # 加载历史日志
)
window.setCentralWidget(log_widget)
window.show()

# 继续使用logger，新日志会实时显示
logger.info("GUI已启动")
logger.warning("这是一条警告")
logger.error("这是一条错误")

# 运行应用
app.exec()

# 清理
HansLoguruUI.listener_process_stop()
```

### 基本使用（命令行）

```python
from hans_loguru import HansLoguru, LogFileConfig
from loguru import logger
import multiprocessing
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()

    # 配置日志文件
    log_files = [
        LogFileConfig("./logs/app.log", level="INFO")
    ]

    # 启动监听进程
    HansLoguru.listener_process_start(log_files=log_files, console_level="INFO")
    HansLoguru.add(HansLoguru.hans_loguru_queue)

    # 使用日志
    logger.info("应用启动")

    # 结束
    HansLoguru.listener_process_stop()
```

### 高级配置 - 多文件多级别

```python
import datetime
from hans_loguru import HansLoguru, LogFileConfig
from loguru import logger

# 生成时间戳
timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# 配置多个日志文件，每个文件不同级别
log_files = [
    # 完整日志 - 记录所有内容
    LogFileConfig(
        file_path=f"./logs/{timestamp}_all.log",
        level="TRACE",              # 记录所有级别
        rotation="50 MB",            # 每50MB轮转一次
        retention="10 days",         # 保留10天
        compression="zip"            # 压缩为zip
    ),

    # 信息日志 - 只记录重要信息
    LogFileConfig(
        file_path=f"./logs/{timestamp}_info.log",
        level="INFO"                 # 只记录INFO及以上
    ),

    # 错误日志 - 只记录错误
    LogFileConfig(
        file_path=f"./logs/{timestamp}_error.log",
        level="ERROR",               # 只记录ERROR及以上
        retention="30 days"          # 错误日志保留30天
    ),
]

# 启动监听进程
# console_level 控制终端显示的日志级别
HansLoguru.listener_process_start(
    log_files=log_files,
    console_level="INFO"  # 终端只显示INFO及以上
)
HansLoguru.add(HansLoguru.hans_loguru_queue)

# 使用示例
logger.trace("详细跟踪信息")      # 只在 all.log
logger.debug("调试信息")          # 只在 all.log
logger.info("一般信息")           # 在 all.log、info.log 和终端
logger.warning("警告信息")        # 在 all.log、info.log 和终端
logger.error("错误信息")          # 在所有文件和终端
logger.critical("严重错误")       # 在所有文件和终端
```

### 多进程使用

```python
def worker_process(queue):
    """子进程函数"""
    # 子进程必须初始化logger
    # 基础用法：只发送日志到主进程
    HansLoguru.add(queue, level="TRACE")

    logger.info("子进程日志")
    logger.error("子进程错误")

def worker_process_with_console(queue):
    """子进程函数 - 带终端输出"""
    # 高级用法：子进程也直接输出到终端
    HansLoguru.add(
        queue,
        level="TRACE",
        console_output=True,    # 启用子进程终端输出
        console_level="INFO"    # 子进程终端只显示INFO及以上
    )

    logger.debug("这条不会在子进程终端显示")
    logger.info("这条会在子进程终端立即显示")
    logger.error("这条也会在子进程终端立即显示")

if __name__ == "__main__":
    freeze_support()

    # 配置日志
    log_files = [LogFileConfig("./logs/app.log", level="INFO")]
    HansLoguru.listener_process_start(log_files=log_files, console_level="INFO")
    HansLoguru.add(HansLoguru.hans_loguru_queue)

    # 创建子进程
    p = multiprocessing.Process(
        target=worker_process_with_console,
        args=(HansLoguru.hans_loguru_queue,)
    )
    p.start()
    p.join()

    # 停止日志
    HansLoguru.listener_process_stop()
```

## API 文档

### LogFileConfig

日志文件配置类。

**参数:**
- `file_path` (str): 日志文件路径
- `level` (str): 日志级别，可选值: TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
- `rotation` (Optional[str]): 日志轮转规则
  - 按大小: `"10 MB"`, `"500 MB"`, `"1 GB"`
  - 按时间: `"12:00"` (每天12点), `"1 week"` (每周), `"1 month"` (每月)
- `retention` (Optional[str]): 日志保留规则
  - 按数量: `"10"` (保留最近10个文件)
  - 按时间: `"7 days"`, `"1 month"`
- `compression` (Optional[str]): 压缩格式
  - 可选值: `"zip"`, `"tar"`, `"tar.gz"`, `"tar.bz2"`, `"tar.xz"`

**示例:**
```python
# 简单配置
LogFileConfig("app.log", level="INFO")

# 完整配置
LogFileConfig(
    file_path="app.log",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    compression="zip"
)
```

### HansLoguru

主日志管理类。

#### listener_process_start()

启动日志监听进程。

**参数:**
- `log_files` (Optional[List[LogFileConfig]]): 日志文件配置列表
- `console_level` (str): 终端输出日志级别，默认 "TRACE"

**返回:**
- `multiprocessing.Queue`: 日志队列

**示例:**
```python
log_files = [
    LogFileConfig("all.log", level="TRACE"),
    LogFileConfig("error.log", level="ERROR")
]
HansLoguru.listener_process_start(
    log_files=log_files,
    console_level="INFO"  # 终端只显示INFO及以上
)
```

#### add()

为子进程配置日志。

**参数:**
- `processing_queue` (multiprocessing.Queue): 日志队列
- `level` (str): 发送到队列的日志级别，默认 "TRACE"
- `console_output` (bool): 是否在子进程中也输出到终端，默认 False
- `console_level` (str): 子进程终端输出的日志级别，默认 "TRACE"

**示例:**
```python
# 基础用法：只发送日志到主进程
HansLoguru.add(queue, level="TRACE")

# 高级用法：子进程也输出到终端，且只显示 INFO 及以上
HansLoguru.add(
    queue,
    level="TRACE",
    console_output=True,
    console_level="INFO"
)
```

**说明:**
- 默认情况下，子进程的日志只会发送到主进程统一处理
- 如果 `console_output=True`，子进程会直接输出到终端，无需等待主进程处理
- 子进程的终端输出格式会显示该子进程的进程ID和线程ID
- 适用场景：
  - `console_output=False`: 适合需要统一管理日志输出的场景
  - `console_output=True`: 适合需要实时查看子进程日志的调试场景

### HansLoguruUI

GUI支持的日志管理类，继承自HansLoguru，添加了日志缓冲区功能。

#### listener_process_start()

启动日志监听进程（带缓冲区支持）。

**参数:**
- `log_files` (Optional[List[LogFileConfig]]): 日志文件配置列表
- `console_level` (str): 终端输出日志级别，默认 "TRACE"
- `buffer_size` (int): 日志缓冲区大小，默认 1000

**返回:**
- `multiprocessing.Queue`: 日志队列

**示例:**
```python
log_files = [
    LogFileConfig("all.log", level="TRACE"),
    LogFileConfig("error.log", level="ERROR")
]
HansLoguruUI.listener_process_start(
    log_files=log_files,
    console_level="INFO",
    buffer_size=2000  # 增加缓冲区大小
)
```

#### add()

为子进程配置日志（自动启用缓冲区）。

参数同 HansLoguru.add()

#### get_log_buffer()

获取日志缓冲区的副本（用于UI组件加载历史日志）。

**返回:**
- `list`: 日志记录列表

**示例:**
```python
history_logs = HansLoguruUI.get_log_buffer()
```

#### clear_log_buffer()

清空日志缓冲区。

**示例:**
```python
HansLoguruUI.clear_log_buffer()
```

#### set_buffer_size()

设置日志缓冲区大小。

**参数:**
- `maxlen` (int): 最大日志条数

**示例:**
```python
# 设置缓冲区最多保存5000条日志
HansLoguruUI.set_buffer_size(5000)
```

### LogWidget (GUI组件)

可移植的日志显示组件，用于在PySide6应用中显示loguru日志。

#### 初始化参数

**参数:**
- `parent` (Optional[QWidget]): 父组件
- `level_colors` (Optional[Dict[str, str]]): 自定义日志级别颜色字典
- `log_format` (Optional[str]): 自定义日志格式字符串
- `default_filter_level` (str): 默认过滤级别，默认 "TRACE"
- `auto_register` (bool): 是否自动注册到loguru，默认 True
- `dark_theme` (bool): 是否使用深色主题，默认 True
- `load_history` (bool): 是否加载历史日志（从缓冲区），默认 True

**示例:**
```python
# 基础使用
log_widget = LogWidget()

# 完整配置
log_widget = LogWidget(
    parent=self,
    default_filter_level="INFO",
    auto_register=True,
    dark_theme=True,
    load_history=True,
    level_colors={
        "INFO": "#00FF00",
        "ERROR": "#FF0000"
    }
)
```

#### 功能特性

1. **实时日志显示** - 所有loguru日志实时显示
2. **彩色日志** - 不同级别用不同颜色：
   - TRACE: 灰色
   - DEBUG: 蓝色
   - INFO: 绿色
   - SUCCESS: 深绿色
   - WARNING: 橙色
   - ERROR: 红色
   - CRITICAL: 深红色
3. **日志级别过滤** - 下拉菜单选择显示级别
4. **清空日志** - 清空按钮清除显示内容
5. **自动滚动** - 可选择是否自动滚动到最新日志
6. **历史日志** - 自动加载创建前的日志（从HansLoguru缓冲区）
7. **线程安全** - 使用Qt信号槽机制

#### 在标签页中使用

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets import LogWidget

class LogTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # 添加日志显示组件
        self.log_widget = LogWidget(
            parent=self,
            default_filter_level="INFO",
            auto_register=True,
            dark_theme=True,
            load_history=True
        )

        layout.addWidget(self.log_widget)
```

#### 测试组件

```bash
# 直接运行测试
python ui/widgets/log_widget.py
```

#### listener_process_stop()

停止日志监听进程。

**示例:**
```python
HansLoguru.listener_process_stop()
```

## 日志级别说明

按严重程度从低到高：

| 级别 | 数值 | 说明 | 使用场景 |
|------|------|------|----------|
| TRACE | 5 | 跟踪 | 最详细的调试信息 |
| DEBUG | 10 | 调试 | 详细的调试信息 |
| INFO | 20 | 信息 | 一般性信息 |
| SUCCESS | 25 | 成功 | 操作成功提示 |
| WARNING | 30 | 警告 | 警告信息 |
| ERROR | 40 | 错误 | 错误信息 |
| CRITICAL | 50 | 严重 | 严重错误 |

## 终端输出配置详解

HansLoguru 提供了灵活的终端输出控制：

### 主进程终端输出
通过 `listener_process_start()` 的 `console_level` 参数控制：
```python
# 终端只显示 INFO 及以上级别
HansLoguru.listener_process_start(log_files=log_files, console_level="INFO")
```

### 子进程终端输出
通过 `add()` 的 `console_output` 和 `console_level` 参数控制：
```python
# 方式1: 子进程不直接输出到终端（默认）
HansLoguru.add(queue)

# 方式2: 子进程也输出到终端
HansLoguru.add(queue, console_output=True, console_level="INFO")
```

### 输出方式对比

| 配置 | 日志流向 | 优点 | 缺点 |
|------|---------|------|------|
| 仅主进程终端 | 子进程 → 队列 → 主进程 → 终端 | 输出统一有序 | 略有延迟 |
| 主+子进程终端 | 子进程 → 队列 → 主进程 → 终端<br>子进程 → 终端（直接） | 实时性好 | 可能乱序 |

### 推荐配置

**调试场景**：子进程启用终端输出，实时查看
```python
HansLoguru.add(queue, console_output=True, console_level="DEBUG")
```

**生产场景**：子进程关闭终端输出，统一管理
```python
HansLoguru.add(queue, console_output=False)
```

## 使用场景示例

### 场景1: 开发环境

开发时需要详细日志，但终端不想看到过多信息：

```python
log_files = [
    LogFileConfig("dev.log", level="TRACE")  # 文件记录所有
]
HansLoguru.listener_process_start(
    log_files=log_files,
    console_level="INFO"  # 终端只看重要的
)
# 主进程终端输出 INFO 及以上
HansLoguru.add(HansLoguru.hans_loguru_queue)
```

### 场景2: 生产环境

生产环境需要分离不同级别的日志便于排查：

```python
log_files = [
    LogFileConfig("prod_info.log", level="INFO", rotation="100 MB", retention="30 days"),
    LogFileConfig("prod_error.log", level="ERROR", retention="90 days", compression="zip")
]
HansLoguru.listener_process_start(
    log_files=log_files,
    console_level="WARNING"  # 终端只显示警告和错误
)
```

### 场景3: 多进程调试

调试多进程程序时，需要实时看到各个子进程的日志：

```python
def worker(queue, worker_id):
    # 启用子进程终端输出，方便实时调试
    HansLoguru.add(
        queue,
        level="TRACE",
        console_output=True,     # 子进程直接输出到终端
        console_level="DEBUG"    # 显示 DEBUG 及以上
    )

    logger.debug(f"Worker {worker_id} 初始化完成")
    logger.info(f"Worker {worker_id} 开始工作")
    # ... 工作逻辑 ...
    logger.info(f"Worker {worker_id} 完成工作")

# 主进程配置
log_files = [LogFileConfig("debug.log", level="TRACE")]
HansLoguru.listener_process_start(log_files=log_files, console_level="DEBUG")
HansLoguru.add(HansLoguru.hans_loguru_queue)

# 启动多个子进程
for i in range(4):
    p = multiprocessing.Process(target=worker, args=(HansLoguru.hans_loguru_queue, i))
    p.start()
```

### 场景4: 性能测试

需要详细日志但要控制文件大小：

```python
log_files = [
    LogFileConfig(
        "perf.log",
        level="DEBUG",
        rotation="50 MB",      # 自动轮转
        retention="5",         # 只保留最近5个文件
        compression="zip"      # 压缩节省空间
    )
]
HansLoguru.listener_process_start(log_files=log_files, console_level="ERROR")
# 子进程不输出到终端，减少性能影响
HansLoguru.add(HansLoguru.hans_loguru_queue, console_output=False)
```

## 注意事项

1. **多进程使用**: 每个子进程必须调用 `HansLoguru.add()` 初始化
2. **freeze_support**: Windows下使用多进程时，主程序需要调用 `freeze_support()`
3. **停止监听**: 程序结束前务必调用 `HansLoguru.listener_process_stop()`
4. **日志级别**: 文件和终端的日志级别可以不同，灵活配置
5. **性能考虑**: 轮转和压缩会占用一定CPU，根据实际情况配置

## 迁移指南

从旧版本迁移到新版本：

### 旧版本代码
```python
# 旧版本
HansLoguru.listener_process_start("./logs/app.log")
```

### 新版本代码
```python
# 新版本 - 方式1：快速迁移
log_files = [LogFileConfig("./logs/app.log", level="TRACE")]
HansLoguru.listener_process_start(log_files=log_files, console_level="TRACE")

# 新版本 - 方式2：利用新功能
log_files = [
    LogFileConfig("./logs/app.log", level="INFO"),
    LogFileConfig("./logs/error.log", level="ERROR")
]
HansLoguru.listener_process_start(log_files=log_files, console_level="INFO")
```

## 运行示例

查看 [example_usage.py](example_usage.py) 文件获取完整的使用示例。

```bash
python example_usage.py
```

## 许可证

本项目使用与主项目相同的许可证。
