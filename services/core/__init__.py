# services/core/__init__.py
"""核心服务模块.

本模块提供核心服务，包括：
    - ConfigService: 配置服务，处理配置的加载、保存和验证
    - DEFAULT_CONFIG: 默认配置常量
    - ConfigValidator: 配置验证器
    - ValidationError: 配置验证异常
    - ThemeService: 主题管理服务

.. note:: 对外只暴露必要的接口，隐藏内部实现细节
"""

from .config import ConfigService, DEFAULT_CONFIG, ConfigValidator, ValidationError
from .theme import ThemeService

__all__ = [
    "ConfigService",      # 对外的主要服务接口
    "DEFAULT_CONFIG",     # 配置常量
    "ConfigValidator",    # 验证工具（供高级用户使用）
    "ValidationError",    # 异常类型
    "ThemeService",       # 主题管理服务
]
