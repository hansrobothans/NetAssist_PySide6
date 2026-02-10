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
│       ↑ 绑定 ThemeViewModel.theme_changed 信号            │
├─────────────────────────────────────────────────────────┤
│  ViewModel 层                                            │
│  ThemeViewModel (继承 BaseViewModel)                      │
│       - theme_changed Signal(object)                     │
│       - current_theme property → ThemeData               │
│       - set_theme(name) / toggle_theme()                 │
│       ↑ 调用 ThemeService                                 │
├─────────────────────────────────────────────────────────┤
│  Service 层                                              │
│  ThemeService                                            │
│       - 管理主题数据（THEMES 注册表）                       │
│       - 通过 ConfigService 持久化到 config.json            │
│       ↑ 读写 ConfigData (key: appearance.theme)           │
├─────────────────────────────────────────────────────────┤
│  Model 层                                                │
│  ThemeData (frozen dataclass) + LIGHT_THEME / DARK_THEME │
└─────────────────────────────────────────────────────────┘
```

## 数据流

```
用户点击侧边栏底部灯泡按钮
  → Sidebar.theme_clicked 信号
    → MainWindow._on_theme_clicked()
      → ThemeViewModel.toggle_theme()
        → ThemeService.toggle_theme()  (dark↔light, 持久化到 config.json)
        → ThemeViewModel emit theme_changed(ThemeData)
          → MainWindow._apply_theme(theme)
            → setStyleSheet(AppStyles.main_window(theme))   # 全局 QSS
            → TitleBar.apply_theme(theme)                   # 自绘标签栏
            → Sidebar.apply_theme(theme)                    # SVG 图标颜色
            → AddTabMenu.apply_theme(theme)                 # 菜单样式
            → 遍历所有已打开标签页 .apply_theme(theme)        # PlaceholderTab / LogTab
```

## 实施文件清单

### 新建文件

| 文件 | 说明 | 状态 |
|------|------|------|
| `models/theme_data.py` | ThemeData frozen dataclass + LIGHT/DARK 预设 + THEMES 注册表 | done |
| `services/core/theme/__init__.py` | 模块导出 ThemeService | done |
| `services/core/theme/theme_service.py` | ThemeService：主题管理、持久化 | done |
| `viewmodels/theme_viewmodel.py` | ThemeViewModel：Qt 信号桥接 | done |

### 改造文件

| 文件 | 改动内容 | 状态 |
|------|---------|------|
| `views/styles/app_styles.py` | 颜色常量 → `main_window(t)` / `menu_style(t)` / `log_text_edit(t)` 等工厂方法 | done |
| `views/widgets/title_bar.py` | TitleTabBar/TitleBarButton 增加 `apply_theme()`，自绘颜色改为实例属性 | done |
| `views/sidebar/sidebar_button.py` | 增加 `apply_theme()`，图标颜色从 ThemeData 获取 | done |
| `views/sidebar/sidebar.py` | 增加 `theme_clicked` 信号 + 灯泡按钮 + `apply_theme()` 遍历子按钮 | done |
| `views/sidebar/add_tab_menu.py` | 增加 `apply_theme()`，菜单 QSS 从 ThemeData 生成 | done |
| `views/tabs/placeholder_tab.py` | 增加 `apply_theme()`，标题/描述颜色从 ThemeData 获取 | done |
| `views/tabs/log_tab.py` | 增加 `apply_theme()` 透传到 LogWidget | done |
| `views/widgets/log_widget.py` | 增加 `apply_theme()` 根据 theme.name 切换 dark/light | done |
| `views/main_window.py` | 创建 ThemeViewModel，连接信号，`_apply_theme()` 全局分发 | done |
| `services/container/factory.py` | 懒加载创建 ThemeService | done |
| `services/container/service_container.py` | 暴露 `theme` 属性 | done |
| `services/core/__init__.py` | 导出 ThemeService | done |
| `services/core/config/defaults.py` | 增加 `appearance.theme` 默认配置 | done |
| `configs/config.json` | 增加 `appearance.theme` 字段 | done |
| `resources/icons/antd_icons.py` | 增加 `bulb` 灯泡图标 (BulbOutlined) | done |
| `viewmodels/__init__.py` | 导出 ThemeViewModel，移除不存在的旧 ViewModel | done |

## ThemeData 语义化令牌一览

```python
@dataclass(frozen=True)
class ThemeData:
    name: str                    # "dark" / "light"

    # 基础
    window_bg, text_primary, text_secondary, border

    # 侧边栏
    sidebar_bg, sidebar_icon, sidebar_icon_hover, sidebar_hover_bg

    # 标题栏 / 标签页
    titlebar_bg, tab_bg, tab_active_bg, tab_hover_bg
    tab_text, tab_active_text, tab_accent

    # 窗口控制按钮
    win_btn_icon, win_btn_icon_hover, win_btn_hover_bg
    close_btn_hover_bg, close_btn_pressed_bg

    # 内容区
    content_bg

    # 菜单
    menu_bg, menu_text, menu_hover_bg, menu_border, menu_separator, menu_disabled_text

    # 状态色（默认值，不随主题变化）
    color_primary, color_success, color_danger, color_warning, color_info

    # 通用控件
    input_bg, input_border, input_focus_border
    input_disabled_bg, input_disabled_text
    button_disabled_bg, button_disabled_text

    # 日志区域
    log_bg, log_text, log_border

    # 占位标签页
    placeholder_title_color, placeholder_desc_color
```

## 关键设计决策

- **为什么不用 QPalette**：QPalette 对自定义控件和 QSS 的覆盖行为不一致，且无法控制 SVG 图标颜色。语义化令牌 + QSS 模板更可控。
- **为什么用信号而不是重启应用**：用户体验更好，实时切换无需重启。
- **为什么 ThemeService 和 ThemeViewModel 分离**：Service 层纯逻辑（数据管理 + 持久化），ViewModel 层负责 Qt 信号绑定，符合 MVVM 分层。
- **为什么 ThemeData 用 frozen=True**：主题实例不可变，切换时整体替换，避免局部修改导致状态不一致。
- **为什么各组件用 `apply_theme()` 方法而不是直接连接信号**：MainWindow 统一分发，控制应用顺序（先全局 QSS → 再自绘组件 → 再子标签页），避免信号连接散落各处。

## 扩展指南

### 添加新主题
1. 在 `models/theme_data.py` 中创建新的 `ThemeData` 实例
2. 添加到 `THEMES` 字典中
3. 无需修改其他代码

### 新组件支持主题
1. 组件实现 `apply_theme(theme: ThemeData)` 方法
2. 在 `MainWindow._apply_theme()` 中调用该方法
3. 如果是标签页，会被自动遍历调用
