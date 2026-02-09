# services/core/theme/theme_service.py
"""主题管理服务.

职责：
    - 管理当前主题状态
    - 通过 ConfigService 持久化主题选择
    - 提供主题查询和切换接口（纯逻辑，不含 Qt 信号）
"""

from typing import TYPE_CHECKING

from loguru import logger

from models.theme_data import ThemeData, THEMES, DARK_THEME

if TYPE_CHECKING:
    from services.core.config import ConfigService


class ThemeService:
    """主题管理服务.

    纯逻辑层，不依赖 Qt。ViewModel 负责信号广播。
    """

    CONFIG_KEY = "appearance.theme"

    def __init__(self, config: "ConfigService"):
        """初始化主题服务.

        :param config: 配置服务实例
        :type config: ConfigService
        """
        logger.trace("")
        self._config = config

        # 从配置读取主题名称，默认 dark
        theme_name = self._config.config.get(self.CONFIG_KEY, "dark")
        self._current_theme: ThemeData = THEMES.get(theme_name, DARK_THEME)

        logger.info(f"ThemeService 已初始化，当前主题: {self._current_theme.name}")

    @property
    def current_theme(self) -> ThemeData:
        """获取当前主题."""
        return self._current_theme

    @property
    def theme_name(self) -> str:
        """获取当前主题名称."""
        return self._current_theme.name

    def set_theme(self, name: str) -> ThemeData:
        """设置主题.

        :param name: 主题名称 ("light" / "dark")
        :type name: str
        :return: 新的主题数据
        :rtype: ThemeData
        :raises ValueError: 未知的主题名称
        """
        if name not in THEMES:
            raise ValueError(f"未知主题: {name}，可选: {list(THEMES.keys())}")

        self._current_theme = THEMES[name]

        # 持久化
        self._config.config.set(self.CONFIG_KEY, name)
        self._config.save()

        logger.info(f"主题已切换为: {name}")
        return self._current_theme

    def toggle_theme(self) -> ThemeData:
        """在 light / dark 之间切换.

        :return: 切换后的主题数据
        :rtype: ThemeData
        """
        new_name = "light" if self._current_theme.name == "dark" else "dark"
        return self.set_theme(new_name)

    def get_available_themes(self) -> list[str]:
        """获取所有可用主题名称.

        :return: 主题名称列表
        :rtype: list[str]
        """
        return list(THEMES.keys())
