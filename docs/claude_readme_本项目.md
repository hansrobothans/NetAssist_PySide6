# NetAssist_PySide6 - 调试助手工具

## 项目概述

基于 PySide6 的桌面调试助手工具，参照 electerm 的 UI 风格。采用 MVVM 架构，无边框窗口 + 自定义标题栏 + 侧边栏 + 多标签页布局。

**版本:** 1.0.0
**应用名称:** 调试工具

## 技术栈

- **UI框架:** PySide6 >= 6.5.0
- **日志:** loguru >= 0.7.0 + 自定义 HansLoguru
- **架构模式:** MVVM + 依赖注入 + 服务工厂

## 目录结构

```
NetAssist_PySide6/
├── main.py                     # 应用入口
├── version.py                  # 版本信息
├── requirements.txt            # 依赖列表
├── configs/                    # 配置文件
│   ├── config.json             # 主配置（含 appearance.theme）
│   └── cus_config.json         # 自定义配置
├── lib/                        # 第三方/自定义库
│   └── hans_loguru/            # 日志框架
│       ├── hans_loguru.py      # 核心日志类
│       └── hans_loguru_ui.py   # UI集成日志类
├── models/                     # 数据模型
│   ├── config_data.py          # 配置数据模型
│   └── theme_data.py           # 主题数据模型（ThemeData + LIGHT/DARK 预设）
├── resources/                  # 资源文件
│   └── icons/
│       └── antd_icons.py       # Ant Design SVG 图标集
├── services/                   # 业务逻辑层
│   ├── container/              # 依赖注入容器
│   │   ├── service_container.py
│   │   └── factory.py
│   └── core/                   # 核心服务
│       ├── config/             # 配置服务
│       │   ├── config_service.py
│       │   ├── defaults.py
│       │   └── validators.py
│       └── theme/              # 主题服务
│           └── theme_service.py
├── viewmodels/                 # MVVM ViewModel层
│   ├── base_viewmodel.py       # 基础ViewModel
│   └── theme_viewmodel.py      # 主题ViewModel
├── views/                      # UI视图层
│   ├── main_window.py          # 主窗口（无边框 + Win32原生事件）
│   ├── sidebar/                # 侧边栏
│   │   ├── sidebar.py          # 侧边栏组件
│   │   ├── sidebar_button.py   # 侧边栏按钮
│   │   └── add_tab_menu.py     # 添加标签页菜单
│   ├── tabs/                   # 标签页
│   │   ├── log_tab.py          # 日志标签页
│   │   └── placeholder_tab.py  # 占位标签页
│   ├── widgets/                # 自定义控件
│   │   ├── title_bar.py        # 自定义标题栏（标签页 + 导航 + 窗口控制）
│   │   ├── log_widget.py       # 日志控件
│   │   └── widget_factory.py   # 控件工厂
│   └── styles/                 # 样式
│       └── app_styles.py       # 应用样式（主题化 QSS 工厂方法）
└── tools/                      # 工具脚本
    ├── build_nuitka_debug.bat
    └── build_nuitka_standalone.bat
```

## 架构设计

### 分层架构

```
Views (UI) → ViewModels (逻辑) → Services (业务) → Models (数据)
```

### 服务层级

- **Level 0:** 独立服务 - Config, Theme
- **Level 1:** 业务服务 (依赖 Level 0)
- **Level 2:** 复合服务 (依赖多个 Level 1)

### 关键类

| 类名 | 文件 | 职责 |
|------|------|------|
| `MainWindow` | views/main_window.py | 主窗口，无边框，标签页管理，主题分发 |
| `TitleBar` | views/widgets/title_bar.py | 自定义标题栏，内嵌标签页 + 导航按钮 + 窗口控制 |
| `TitleTabBar` | views/widgets/title_bar.py | 自绘标签页栏（paintEvent），支持拖拽排序 |
| `TabBarScrollContainer` | views/widgets/title_bar.py | 标签页滚动容器，支持溢出滚动 |
| `Sidebar` | views/sidebar/sidebar.py | 左侧工具栏，功能按钮入口 |
| `ThemeData` | models/theme_data.py | 主题颜色令牌（frozen dataclass） |
| `ThemeService` | services/core/theme/theme_service.py | 主题管理 + 持久化 |
| `ThemeViewModel` | viewmodels/theme_viewmodel.py | 主题 Qt 信号桥接 |
| `BaseViewModel` | viewmodels/base_viewmodel.py | ViewModel基类 |
| `ServiceContainer` | services/container/service_container.py | 依赖注入容器 |
| `ServiceFactory` | services/container/factory.py | 服务工厂，懒加载 |
| `ConfigService` | services/core/config/config_service.py | 配置管理 |
| `AppStyles` | views/styles/app_styles.py | 主题化 QSS 工厂方法 |

## UI 布局

### 整体结构

```
┌──────────────────────────────────────────────────────────┐
│ Sidebar │ TitleBar                                        │
│  (左侧)  │ [标签栏][+] [---弹性空间---] [<][>][V] [_][□][×] │
│         ├────────────────────────────────────────────────│
│         │ ContentStack (QStackedWidget)                   │
│         │   由标签栏 currentChanged 控制切换               │
└──────────────────────────────────────────────────────────┘
```

### 标题栏组件

- **TitleTabBar**: 自绘标签页（paintEvent），支持关闭、拖拽排序、编号徽章、类型图标
- **TabBarScrollContainer**: 包裹标签栏，标签溢出时支持滚动
- **AddTabButton (+)**: 紧贴标签栏右侧，弹出添加菜单
- **TabNavButton (<, >, V)**: 标签页导航按钮
  - `<` 向左滚动标签栏
  - `>` 向右滚动标签栏
  - `V` 下拉列表显示所有标签，带全局序号，当前标签有 ● 标记
- **窗口控制按钮**: 最小化、最大化/还原、关闭
- **拖拽移动**: 空白区域拖拽使用 QWindow.startSystemMove()，支持 Aero Snap
- **双击最大化**: 空白区域双击切换最大化/还原

### 无边框窗口

- `FramelessWindowHint` 去掉系统标题栏
- Win32 `WS_THICKFRAME` 恢复边缘缩放和 Aero Snap
- `WM_NCCALCSIZE` 阻止系统绘制标题栏
- `WM_NCHITTEST` 处理边缘缩放区域

## 主题系统

详见 `claude_readme_theme.md`。

- **ThemeData**: frozen dataclass，语义化颜色令牌
- **内置主题**: LIGHT_THEME / DARK_THEME
- **切换方式**: 侧边栏灯泡按钮 → ThemeViewModel.toggle_theme()
- **应用流程**: MainWindow._apply_theme() 统一分发到所有组件
- **持久化**: config.json → appearance.theme

## 图标系统

使用 Ant Design Outlined 风格 SVG 图标，定义在 `resources/icons/antd_icons.py`。

所有图标使用 `fill="currentColor"`，运行时替换为主题颜色。

可用图标: menu, plus-circle, book, setting, file-text, info-circle, global, usb, api, console, cloud-server, send, plus, window-minimize, window-maximize, window-restore, window-close, chevron-left, chevron-right, chevron-down, bulb, chip, swap, toggle

### 标签页图标映射

每个标签页左侧显示：**编号徽章**（electerm 风格药丸形蓝色背景 + 白色数字）+ **类型图标** + **标签文字**。

编号为全局自增编号（1, 2, 3...），创建时分配，删除标签后编号不变，只增不减。

| 标签类型 | 图标名 | 图标含义 |
|---------|--------|---------|
| tcp_server | cloud-server | 云服务器 |
| tcp_client | send | 发送 |
| udp_server | cloud-server | 云服务器 |
| udp_client | send | 发送 |
| serial | api | 接口链路 |
| i2c | chip | 总线拓扑（节点连线） |
| spi | swap | 方波时钟信号 |
| gpio | toggle | 开关控制 |
| log | file-text | 文件日志 |

图标映射定义在 `AddTabMenu.TAB_ICONS`（`views/sidebar/add_tab_menu.py`）。

标签元数据通过 `QTabBar.setTabData()` 存储 `{"type", "icon", "number"}`，编号在创建时由 `MainWindow._next_tab_number` 自增计数器分配，只增不减。

## 配置说明

配置文件位于 `configs/config.json`，支持：

- **output:** 输出路径配置 (日志)
- **logging:** 日志配置 (级别、轮转、保留策略)
- **appearance.theme:** 主题名称 ("dark" / "light")

配置访问支持点号语法：`config.get("server.port")`

## 日志系统

使用自定义 HansLoguru 框架：

- 多文件日志 (all.log, info.log, error.log)
- 日志轮转和保留策略
- 实时 UI 显示
- 进程/线程信息追踪

## 开发指南

### 添加新服务

1. 在 `services/core/` 下创建服务类
2. 在 `ServiceFactory` 中添加创建方法
3. 在 `ServiceContainer` 中暴露访问接口

### 添加新标签页

1. 在 `views/tabs/` 下创建标签页类
2. 实现 `apply_theme(theme: ThemeData)` 方法
3. 在 `AddTabMenu.TAB_TYPES` 中注册类型名称
4. 在 `AddTabMenu.TAB_ICONS` 中注册类型图标
5. MainWindow._apply_theme() 会自动遍历调用

### 新组件支持主题

1. 组件实现 `apply_theme(theme: ThemeData)` 方法
2. 在 `MainWindow._apply_theme()` 中调用该方法

### 添加新图标

1. 在 `resources/icons/antd_icons.py` 的 `ICONS` 字典中添加 SVG 字符串
2. 使用 `fill="currentColor"` 支持动态颜色
3. 通过 `TitleBarButton` 或 `SidebarButton` 的 icon_name 参数引用

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

## 当前状态

- ✅ 核心架构完成（MVVM + 依赖注入）
- ✅ 日志系统完成
- ✅ 配置管理完成
- ✅ 无边框窗口 + 自定义标题栏
- ✅ 侧边栏 + 多标签页布局
- ✅ 主题系统（dark/light 切换）
- ✅ 标签页导航（滚动 + 下拉列表）
- ✅ 标签页图标 + 编号徽章（electerm 风格）
- ⏳ 调试助手功能 (开发中)
