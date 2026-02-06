# services/container/service_container.py
"""服务容器主类模块.

本模块提供 ServiceContainer 类，专注于服务的创建和依赖注入。
服务的启动/停止由服务自己管理，信号连接由使用者管理。

组合模式：
    - ServiceFactory: 服务创建
"""

from typing import TYPE_CHECKING, Optional

from loguru import logger
from PySide6.QtCore import QObject

from services.container.factory import ServiceFactory

if TYPE_CHECKING:
    from services.core import ConfigService
    from services.network import TcpClientService, TcpServerService
    from services.hardware import Opt4001Service
    from services.protocol import ProtocolService
    from services.detection.base import BaseDetector
    from services.detection import ImageStickingDetectionService


class ServiceContainer(QObject):
    """服务容器 - 专注于服务的创建和依赖注入.

    职责：
        - 创建服务实例（懒加载）
        - 依赖注入
        - 清理服务引用

    不负责：
        - 服务的启动/停止（由服务自己管理）
        - 信号连接（由使用者管理）

    使用示例::

        # 创建配置服务
        config_service = ConfigService("./configs/config.json")

        # 创建服务容器
        container = ServiceContainer(config=config_service)

        # 获取服务（懒加载创建）
        detection = container.create_detection_service("sensor")

        # 直接调用服务的启动/停止方法
        detection.start()
        detection.stop()

        # 退出时清理
        container.cleanup()
    """

    def __init__(self, config: "ConfigService", parent: Optional[QObject] = None):
        """初始化服务容器.

        :param config: 配置服务实例
        :type config: ConfigService
        :param parent: 父 QObject
        :type parent: Optional[QObject]
        """
        super().__init__(parent)
        logger.trace("")

        # Core (构造时注入)
        self._config = config

        # 初始化服务工厂
        self._factory = ServiceFactory(config=config)

        logger.info("ServiceContainer 已创建")

    # ==================== 属性 ====================
    @property
    def config(self) -> "ConfigService":
        """获取配置服务."""
        return self._config

    # ==================== Network 服务 ====================
    
    # ==================== Hardware 服务 ====================
    

    # ==================== Protocol 服务 ====================
    

    
    # ==================== 生命周期管理 ====================
    def cleanup(self) -> None:
        """清理服务容器.

        ServiceContainer 只负责清理服务引用，
        不负责停止服务和信号连接。
        """
        logger.info("开始清理服务容器...")

        # 清理服务引用
        self._factory.clear_all()

        logger.info("服务容器清理完成")

    def __del__(self) -> None:
        """析构函数."""
        logger.trace("ServiceContainer 析构")
