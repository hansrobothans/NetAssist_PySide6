# 主题切换架构方案（MVVM + Service）

## 当前问题

1. **颜色硬编码分散**：`AppStyles` 中定义颜色常量，但 `TitleTabBar`、`SidebarButton`、`AddTabMenu`、`PlaceholderTab` 等组件内部也各自硬编码颜色值。
2. **TitleTabBar 使用 `paintEvent` 自绘**：颜色直接写在绘制逻辑里，QSS 无法覆盖。
3. **SVG 图标颜色**：各组件自行传入颜色字符串，没有统一来源。
4. **LogWidget 有独立的 dark/light 切换**，但与全局无关。
5. **配置文件中没有主题字段**。

## 架构设计（MVVM + Service 分层）

```
┌─────────────────────────────────────────────────────────┐
│  View 层                                                 │
│  MainWindow / TitleBar / Sidebar / Tabs / LogWidget      │
│       ↑ 绑定 ThemeViewModel 信号                          │
├─────────────────────────────────────────────────────────┤
│  ViewModel 层                                            │
│  ThemeViewModel (继承 BaseViewModel)                      │
│       - theme_changed Signal(Theme)                      │
│       - current_theme property                           │
│       - set_theme(name) / toggle_theme()                 │
│       ↑ 调用 ThemeService                                 │
├─────────────────────────────────────────────────────────┤
│  Service 层                                              │
│  ThemeService                                            │
│       - 管理主题数据                                       │
│       - 通过 ConfigService 持久化                          │
│       ↑ 读写 ConfigData                                   │
├─────────────────────────────────────────────────────────┤
│  Model 层                                                │
│  ThemeData (dataclass) + LIGHT_THEME / DARK_THEME 预设    │
└─────────────────────────────────────────────────────────┘
```

## 数据流

```
用户点击切换按钮
  → View 调用 ThemeViewModel.toggle_theme()
    → ThemeViewModel 调用 ThemeService.set_theme("dark")
      → ThemeService 更新内部状态 + ConfigService 持久化
    → ThemeViewModel emit theme_changed(Theme)
      → 各 View 收到信号，重新应用样式
```

## 新增/修改文件清单

| 操作 | 文件 | 说明 |
|------|------|------|
| **新建** | `models/theme_data.py` | Theme dataclass + LIGHT/DARK 预设 |
| **新建** | `services/core/theme/__init__.py` | 模块导出 |
| **新建** | `services/core/theme/theme_service.py` | ThemeService：主题管理服务 |
| **新建** | `viewmodels/theme_viewmodel.py` | ThemeViewModel：主题 ViewModel |
| **改造** | `views/styles/app_styles.py` | 颜色常量 → 接收 Theme 的工厂方法 |
| **改造** | `views/widgets/title_bar.py` | TitleTabBar/TitleBarButton 从 Theme 读取颜色 |
| **改造** | `views/sidebar/sidebar_button.py` | 图标颜色从 Theme 获取 |
| **改造** | `views/sidebar/add_tab_menu.py` | 菜单样式从 Theme 生成 |
| **改造** | `views/tabs/placeholder_tab.py` | 内联样式改为 Theme 驱动 |
| **改造** | `views/widgets/log_widget.py` | 连接全局信号，同步主题 |
| **改造** | `views/main_window.py` | 初始化 ThemeViewModel，连接信号 |
| **改造** | `services/container/factory.py` | 创建 ThemeService |
| **改造** | `services/container/service_container.py` | 暴露 ThemeService |
| **改造** | `services/core/config/defaults.py` | 增加 theme 默认配置 |

## 关键设计决策

- **为什么不用 QPalette**：QPalette 对自定义控件和 QSS 的覆盖行为不一致，且无法控制 SVG 图标颜色。语义化令牌 + QSS 模板更可控。
- **为什么用信号而不是重启应用**：用户体验更好，实时切换无需重启。
- **为什么 ThemeService 和 ThemeViewModel 分离**：Service 层纯逻辑（数据管理 + 持久化），ViewModel 层负责 Qt 信号绑定，符合 MVVM 分层。
