# services/container/factory.py
"""服务创建工厂模块.

职责：
    - 所有服务的创建方法
    - 懒加载单例管理
    - 依赖注入
"""

from typing import TYPE_CHECKING, Dict, Optional

from loguru import logger

if TYPE_CHECKING:
    from services.core import ConfigService
    from services.core.theme import ThemeService


class ServiceFactory:
    """服务创建工厂.

    负责创建和管理所有服务实例：
        - 懒加载创建
        - 依赖注入
        - 单例管理

    服务分层：
        - Level 0: 独立服务（无依赖）- Network, Hardware, Protocol
    """

    def __init__(self, config: "ConfigService"):
        """初始化服务工厂.

        :param config: 配置服务实例
        :type config: ConfigService
        """
        logger.trace("")

        # Core (构造时注入)
        self._config = config

        # 懒加载单例缓存
        self._theme_service: Optional["ThemeService"] = None

    # ==================== 属性 ====================
    @property
    def config(self) -> "ConfigService":
        """获取配置服务."""
        return self._config

    # ==================== Theme 服务 ====================
    @property
    def theme(self) -> "ThemeService":
        """获取主题服务（懒加载）."""
        if self._theme_service is None:
            from services.core.theme import ThemeService
            self._theme_service = ThemeService(config=self._config)
        return self._theme_service

    # ==================== Level 0: Network ====================
    

    # ==================== Level 2: DetectionService ====================
    

    # ==================== 服务实例访问 ====================
    
    # ==================== 清理 ====================
    def clear_all(self) -> None:
        """清理所有服务引用（不调用服务的清理方法）."""
        self._theme_service = None