# services/container/__init__.py
"""服务容器模块.

提供 ServiceContainer 作为统一的服务管理入口。
"""

from services.container.service_container import ServiceContainer

__all__ = ["ServiceContainer"]
