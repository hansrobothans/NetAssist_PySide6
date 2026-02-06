# services/config/validators.py
"""程序配置验证器模块.

本模块提供配置验证功能的简化版实现。
"""

from typing import Any, Dict, List
from loguru import logger


class ValidationError(Exception):
    """配置验证错误异常类.

    当配置验证失败时抛出此异常。
    """
    pass

class ConfigValidator:
    """程序配置验证器类.

    提供配置数据的验证功能。
    """
    @classmethod
    def validate_full_config(cls, config: Dict[str, Any]) -> List[str]:
        """验证完整配置.

        :param config: 待验证的配置字典
        :type config: Dict[str, Any]
        :return: 验证错误信息列表，如果无错误则返回空列表
        :rtype: List[str]
        """
        logger.trace(f"")
        all_errors = []
        return all_errors
