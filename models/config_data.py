# models/config_data.py
"""配置数据模型.

本模块定义了配置管理相关的数据模型，提供配置数据的存储和访问功能。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from pathlib import Path
from loguru import logger


@dataclass
class ConfigData:
    """配置数据模型.

    用于存储和管理应用程序配置数据，支持嵌套的键值对访问。

    属性：
        - data: 配置数据字典
        - file_path: 配置文件路径
        - is_modified: 配置是否已修改
        - is_valid: 配置是否有效
        - validation_errors: 验证错误列表
    """

    # 配置内容
    data: Dict[str, Any] = field(default_factory=dict)

    # 元数据
    file_path: Optional[Path] = None
    is_modified: bool = False
    is_valid: bool = True
    validation_errors: list[str] = field(default_factory=list)

    def __post_init__(self):
        """后初始化处理.

        将字符串类型的file_path转换为Path对象。
        """
        logger.trace(f"")
        if isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)

    def get(self, key_path: str, default: Any = None) -> Any:
        """获取配置值.

        支持点号分隔的路径访问嵌套配置，例如 "server.port"。

        :param key_path: 配置键路径，使用点号分隔
        :type key_path: str
        :param default: 默认值，当键不存在时返回
        :type default: Any
        :return: 配置值或默认值
        :rtype: Any
        """
        logger.trace(f"")
        keys = key_path.split('.')
        value = self.data

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError, IndexError):
            return default

    def set(self, key_path: str, value: Any) -> None:
        """设置配置值.

        支持点号分隔的路径设置嵌套配置。如果中间路径不存在，会自动创建。

        :param key_path: 配置键路径，使用点号分隔
        :type key_path: str
        :param value: 要设置的值
        :type value: Any
        """
        logger.trace(f"")
        keys = key_path.split('.')
        data_ref = self.data

        # 导航到目标位置
        for key in keys[:-1]:
            if key not in data_ref:
                data_ref[key] = {}
            data_ref = data_ref[key]

        # 设置值
        data_ref[keys[-1]] = value
        self.is_modified = True


