# NetAssist_PySide6 - 调试助手工具

## 项目概述

基于 PySide6 的桌面调试助手工具。本项目从残影检测调试工具移植而来，保留了成熟的 MVVM 架构和基础设施，用于开发通用调试助手功能。

**版本:** 1.0.0
**应用名称:** 调试工具

## 技术栈

- **UI框架:** PySide6 >= 6.5.0
- **日志:** loguru >= 0.7.0 + 自定义 HansLoguru
- **架构模式:** MVVM + 依赖注入 + 服务工厂

## 目录结构

```
NetAssist_PySide6/
├── main.py                 # 应用入口
├── version.py              # 版本信息
├── requirements.txt        # 依赖列表
├── configs/                # 配置文件
│   ├── config.json         # 主配置
│   └── cus_config.json     # 自定义配置
├── lib/                    # 第三方/自定义库
│   └── hans_loguru/        # 日志框架
│       ├── hans_loguru.py      # 核心日志类
│       └── hans_loguru_ui.py   # UI集成日志类
├── models/                 # 数据模型
│   └── config_data.py      # 配置数据模型
├── services/               # 业务逻辑层
│   ├── container/          # 依赖注入容器
│   │   ├── service_container.py  # 服务容器
│   │   └── factory.py            # 服务工厂
│   └── core/               # 核心服务
│       └── config/         # 配置服务
│           ├── config_service.py # 配置管理
│           ├── defaults.py       # 默认配置
│           └── validators.py     # 配置验证
├── viewmodels/             # MVVM ViewModel层
│   └── base_viewmodel.py   # 基础ViewModel
├── views/                  # UI视图层
│   ├── main_window.py      # 主窗口
│   ├── tabs/               # 标签页
│   │   └── log_tab.py      # 日志标签页
│   ├── widgets/            # 自定义控件
│   │   └── log_widget.py   # 日志控件
│   └── styles/             # 样式
│       └── app_styles.py   # 应用样式
└── tools/                  # 工具模块
```

## 架构设计

### 分层架构

```
Views (UI) → ViewModels (逻辑) → Services (业务) → Models (数据)
```

### 服务层级

- **Level 0:** 独立服务 - Network, Config
- **Level 1:** 业务服务 (依赖 Level 0)
- **Level 2:** 复合服务 (依赖多个 Level 1)

### 关键类

| 类名 | 文件 | 职责 |
|------|------|------|
| `MainWindow` | views/main_window.py | 主窗口，标签页管理 |
| `BaseViewModel` | viewmodels/base_viewmodel.py | ViewModel基类，信号槽机制 |
| `ServiceContainer` | services/container/service_container.py | 依赖注入容器 |
| `ServiceFactory` | services/container/factory.py | 服务工厂，懒加载 |
| `ConfigService` | services/core/config/config_service.py | 配置管理 |
| `ConfigData` | models/config_data.py | 配置数据模型 |
| `HansLoguruUI` | lib/hans_loguru/hans_loguru_ui.py | UI日志系统 |

## 配置说明

配置文件位于 `configs/config.json`，支持：

- **output:** 输出路径配置 (日志)
- **logging:** 日志配置 (级别、轮转、保留策略)

配置访问支持点号语法：`config.get("server.port")`

## 日志系统

使用自定义 HansLoguru 框架：

- 多文件日志 (all.log, info.log, error.log)
- 日志轮转和保留策略
- 实时 UI 显示
- 进程/线程信息追踪

## 开发指南

### 添加新服务

1. 在 `services/` 下创建服务类
2. 在 `ServiceFactory` 中添加创建方法
3. 在 `ServiceContainer` 中暴露访问接口

### 添加新视图

1. 在 `views/` 下创建视图类
2. 创建对应的 ViewModel (继承 `BaseViewModel`)
3. 在 `MainWindow` 中注册标签页

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

## 项目来源

本项目基于残影检测调试工具的架构移植，保留了：
- MVVM 架构模式
- 依赖注入容器
- HansLoguru 日志系统
- 配置管理系统

## 当前状态

- ✅ 核心架构完成
- ✅ 日志系统完成
- ✅ 配置管理完成
- ⏳ 调试助手功能 (开发中)
