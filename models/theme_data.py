# models/theme_data.py
"""主题数据模型.

定义主题的语义化颜色令牌，以及内置的 Light / Dark 预设。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ThemeData:
    """主题颜色令牌.

    所有颜色值均为 CSS 颜色字符串（如 "#ffffff"）。
    frozen=True 保证主题实例不可变，切换时整体替换。
    """

    name: str

    # ── 基础 ──
    window_bg: str
    text_primary: str
    text_secondary: str
    border: str

    # ── 侧边栏 ──
    sidebar_bg: str
    sidebar_icon: str
    sidebar_icon_hover: str
    sidebar_hover_bg: str

    # ── 标题栏 / 标签页 ──
    titlebar_bg: str
    tab_bg: str
    tab_active_bg: str
    tab_hover_bg: str
    tab_text: str
    tab_active_text: str
    tab_accent: str

    # ── 窗口控制按钮 ──
    win_btn_icon: str
    win_btn_icon_hover: str
    win_btn_hover_bg: str
    close_btn_hover_bg: str
    close_btn_pressed_bg: str

    # ── 内容区 ──
    content_bg: str

    # ── 菜单 ──
    menu_bg: str
    menu_text: str
    menu_hover_bg: str
    menu_border: str
    menu_separator: str
    menu_disabled_text: str

    # ── 状态色（不随主题变化，但放在这里方便统一引用） ──
    color_primary: str = "#2196F3"
    color_success: str = "#4CAF50"
    color_danger: str = "#f44336"
    color_warning: str = "#FF9800"
    color_info: str = "#2196F3"

    # ── 通用控件 ──
    input_bg: str = "#ffffff"
    input_border: str = "#dddddd"
    input_focus_border: str = "#2196F3"
    input_disabled_bg: str = "#f5f5f5"
    input_disabled_text: str = "#999999"
    button_disabled_bg: str = "#cccccc"
    button_disabled_text: str = "#666666"

    # ── 日志区域 ──
    log_bg: str = "#1E1E1E"
    log_text: str = "#D4D4D4"
    log_border: str = "#3C3C3C"

    # ── 占位标签页 ──
    placeholder_title_color: str = "#333333"
    placeholder_desc_color: str = "#888888"


# ══════════════════════════════════════════════
#  内置主题预设
# ══════════════════════════════════════════════

DARK_THEME = ThemeData(
    name="dark",

    # 基础
    window_bg="#1e1e1e",
    text_primary="#d4d4d4",
    text_secondary="#888888",
    border="#3c3c3c",

    # 侧边栏
    sidebar_bg="#1f1f1f",
    sidebar_icon="#888888",
    sidebar_icon_hover="#ffffff",
    sidebar_hover_bg="rgba(255, 255, 255, 0.1)",

    # 标题栏 / 标签页
    titlebar_bg="#2b2b2b",
    tab_bg="#2b2b2b",
    tab_active_bg="#1e1e1e",
    tab_hover_bg="#3c3c3c",
    tab_text="#888888",
    tab_active_text="#d4d4d4",
    tab_accent="#0078d4",

    # 窗口控制按钮
    win_btn_icon="#888888",
    win_btn_icon_hover="#ffffff",
    win_btn_hover_bg="rgba(255, 255, 255, 0.1)",
    close_btn_hover_bg="#e81123",
    close_btn_pressed_bg="#bf0f1d",

    # 内容区
    content_bg="#1e1e1e",

    # 菜单
    menu_bg="#2b2b2b",
    menu_text="#cccccc",
    menu_hover_bg="#3c3c3c",
    menu_border="#3c3c3c",
    menu_separator="#3c3c3c",
    menu_disabled_text="#888888",

    # 通用控件
    input_bg="#2b2b2b",
    input_border="#3c3c3c",
    input_focus_border="#0078d4",
    input_disabled_bg="#2b2b2b",
    input_disabled_text="#555555",
    button_disabled_bg="#3c3c3c",
    button_disabled_text="#666666",

    # 日志
    log_bg="#1E1E1E",
    log_text="#D4D4D4",
    log_border="#3C3C3C",

    # 占位标签页
    placeholder_title_color="#d4d4d4",
    placeholder_desc_color="#888888",
)

LIGHT_THEME = ThemeData(
    name="light",

    # 基础
    window_bg="#f0f0f0",
    text_primary="#333333",
    text_secondary="#666666",
    border="#dddddd",

    # 侧边栏
    sidebar_bg="#1f1f1f",
    sidebar_icon="#888888",
    sidebar_icon_hover="#ffffff",
    sidebar_hover_bg="rgba(255, 255, 255, 0.1)",

    # 标题栏 / 标签页
    titlebar_bg="#f0f0f0",
    tab_bg="#f0f0f0",
    tab_active_bg="#ffffff",
    tab_hover_bg="#e5e5e5",
    tab_text="#666666",
    tab_active_text="#333333",
    tab_accent="#0078d4",

    # 窗口控制按钮
    win_btn_icon="#888888",
    win_btn_icon_hover="#ffffff",
    win_btn_hover_bg="rgba(0, 0, 0, 0.1)",
    close_btn_hover_bg="#e81123",
    close_btn_pressed_bg="#bf0f1d",

    # 内容区
    content_bg="#ffffff",

    # 菜单
    menu_bg="#f0f0f0",
    menu_text="#333333",
    menu_hover_bg="#e5e5e5",
    menu_border="#dddddd",
    menu_separator="#dddddd",
    menu_disabled_text="#888888",

    # 通用控件（保持默认值）

    # 日志
    log_bg="#FFFFFF",
    log_text="#000000",
    log_border="#CCCCCC",

    # 占位标签页
    placeholder_title_color="#333333",
    placeholder_desc_color="#888888",
)

# 主题注册表
THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
}
