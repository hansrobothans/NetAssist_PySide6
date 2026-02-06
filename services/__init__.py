# services/__init__.py
"""服务层模块.

本模块提供应用程序的业务逻辑服务层。

.. note:: MVVM架构中的Service Layer，负责业务逻辑处理
"""

# 服务容器
from .container import ServiceContainer


# 配置服务
from .core import ConfigService



__all__ = [
    # 服务容器
    'ServiceContainer',


    # 配置服务
    'ConfigService',

]
