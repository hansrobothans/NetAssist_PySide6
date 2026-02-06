# services/config/config_service.py
"""配置服务模块.

本模块提供配置的加载、保存、验证和访问功能。
采用依赖注入模式，通过构造函数接收配置文件路径。
"""

import json
import os
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from copy import deepcopy
from loguru import logger

from models.config_data import ConfigData
from .defaults import DEFAULT_CONFIG
from .validators import ConfigValidator, ValidationError


class ConfigService:
    """配置服务类.

    MVVM架构中的服务层组件，负责配置的加载、验证和访问。

    使用方法：
        # 创建服务实例（自动加载配置文件）
        config_service = ConfigService("./configs/config.json")

        # 通过实例访问配置
        ip = config_service.hawk_ip
        port = config_service.hawk_port
        paths = config_service.output_paths
        log_files = config_service.get_log_file_configs()
        console_config = config_service.get_console_config()
    """

    def __init__(self, config_path: str):
        """初始化配置服务实例.

        从指定路径加载配置文件，如果文件不存在或加载失败则使用默认配置。

        :param config_path: 配置文件路径
        :type config_path: str
        """
        logger.trace("初始化 ConfigService 实例")

        # 加载配置
        try:
            if os.path.exists(config_path):
                self._config: ConfigData = self._load_from_file(config_path)
                logger.info(f"已加载配置文件: {config_path}")
            else:
                self._config = self._create_default()
                logger.info("配置文件不存在，使用默认配置")
        except Exception as e:
            logger.opt(exception=e).warning("加载配置文件失败，使用默认配置")
            self._config = self._create_default()

        # 初始化输出路径
        self._output_paths: Dict[str, Path] = self._init_output_paths()
        logger.info(f"ConfigService 已初始化，输出目录: {self._output_paths['root']}")

    # ==================== 实例属性 ====================
    @property
    def config(self) -> ConfigData:
        """获取配置数据对象.

        :return: 配置数据对象
        :rtype: ConfigData
        """
        return self._config

    @property
    def output_paths(self) -> Dict[str, Path]:
        """获取输出路径字典.

        :return: 包含各个输出路径的字典 {"root", "logs"}
        :rtype: Dict[str, Path]
        """
        return self._output_paths

    @property
    def logging_config(self) -> Dict:
        """获取日志配置.

        :return: 日志配置字典
        :rtype: Dict
        """
        return self._config.get("logging", {})

    @property
    def log_level(self) -> str:
        """获取全局日志级别.

        :return: 日志级别（如 'INFO', 'DEBUG' 等）
        :rtype: str
        """
        return self._config.get("logging.level", "INFO")

    # ==================== 实例方法 ====================
    def get_log_file_configs(self):
        """获取日志文件配置列表.

        从配置数据中提取日志文件配置，并转换为HansLoguru的LogFileConfig对象列表。

        :return: LogFileConfig对象列表
        :rtype: list
        """
        from lib.hans_loguru import LogFileConfig

        logger.trace("获取日志文件配置")
        log_files = []

        # 获取日志文件配置列表
        files_config = self._config.get("logging.files", [])

        for file_cfg in files_config:
            # 检查是否启用
            if not file_cfg.get("enabled", True):
                logger.debug(f"日志文件 {file_cfg.get('name', 'unknown')} 已禁用，跳过")
                continue

            # 构建日志文件路径
            filename = file_cfg.get("filename", "app.log")
            file_path = str(self._output_paths["logs"] / filename)

            # 获取日志级别（如果为null则使用全局级别）
            level = file_cfg.get("level")
            if level is None:
                level = self._config.get("logging.level", "INFO")

            # 创建LogFileConfig对象
            log_file = LogFileConfig(
                file_path=file_path,
                level=level,
                rotation=file_cfg.get("rotation"),
                retention=file_cfg.get("retention"),
                compression=file_cfg.get("compression"),
                format=file_cfg.get("format")
            )

            log_files.append(log_file)
            logger.debug(f"已添加日志文件配置: {file_cfg.get('name', 'unknown')} -> {file_path} (级别: {level})")

        logger.info(f"已加载 {len(log_files)} 个日志文件配置")
        return log_files

    def get_console_config(self):
        """获取控制台日志配置.

        从配置数据中提取控制台配置，并转换为HansLoguru的ConsoleConfig对象。

        :return: ConsoleConfig对象
        :rtype: ConsoleConfig
        """
        from lib.hans_loguru import ConsoleConfig

        logger.trace("获取控制台日志配置")

        # 获取控制台配置字典
        console_dict = self._config.get("logging.console", {})

        # 获取各个配置项（如果没有配置则使用默认值）
        enabled = console_dict.get("enabled", True)
        level = console_dict.get("level")
        if level is None:
            # 如果控制台配置中没有level，使用全局level
            level = self._config.get("logging.level", "INFO")
        format_str = console_dict.get("format")
        colorize = console_dict.get("colorize", True)

        # 创建ConsoleConfig对象
        console_config = ConsoleConfig(
            enabled=enabled,
            level=level,
            format=format_str,
            colorize=colorize
        )

        logger.debug(f"已加载控制台配置 (启用: {enabled}, 级别: {level}, 颜色: {colorize})")
        return console_config

    def save(self, file_path: Optional[Union[str, Path]] = None) -> None:
        """保存配置到文件.

        :param file_path: 保存路径，如果为None则使用config中的路径
        :type file_path: Optional[Union[str, Path]]
        :raises ValueError: 当未指定保存路径时
        """
        save_path = Path(file_path) if file_path else self._config.file_path

        if save_path is None:
            raise ValueError("未指定保存路径")

        logger.trace(f"保存配置到文件: {save_path}")

        try:
            # 验证配置
            errors = ConfigValidator.validate_full_config(self._config.data)
            if errors:
                logger.warning(f"配置验证警告: {errors}")

            # 确保目录存在
            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self._config.data, f, indent=4, ensure_ascii=False)

            self._config.file_path = save_path
            self._config.is_modified = False
            logger.info(f"配置已保存到: {save_path}")

        except Exception as e:
            logger.opt(exception=e).error("保存配置文件失败")
            raise

    def validate(self) -> bool:
        """验证配置数据.

        :return: 配置是否有效
        :rtype: bool
        """
        logger.trace("验证配置数据")
        errors = ConfigValidator.validate_full_config(self._config.data)
        self._config.validation_errors = errors
        self._config.is_valid = len(errors) == 0
        return self._config.is_valid

    def export_to_json(self) -> str:
        """导出为JSON字符串.

        :return: JSON格式的配置字符串
        :rtype: str
        """
        logger.trace("导出配置为JSON")
        return json.dumps(self._config.data, indent=4, ensure_ascii=False)

    # ==================== 内部方法 ====================
    def _init_output_paths(self) -> Dict[str, Path]:
        """初始化输出路径.

        根据配置生成输出路径字典。支持自动生成时间戳目录和手动指定目录两种模式。

        :return: 包含各个输出路径的字典
        :rtype: Dict[str, Path]
        """
        logger.trace("初始化输出路径")

        # 读取配置
        auto_generate = self._config.get("output.auto_generate", True)
        root_dir = self._config.get("output.root_dir", "./resources/output")
        manual_dir = self._config.get("output.manual_dir")

        # 获取子目录配置
        logs_subdir = self._config.get("output.subdirs.logs", "logs")

        # 根据模式确定根目录
        if auto_generate:
            # 自动生成模式：在根目录下创建时间戳子目录
            time_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            root_path = Path(root_dir) / time_str
            logger.info(f"使用自动生成模式，时间戳: {time_str}")
        else:
            # 手动模式：使用指定目录
            if manual_dir:
                root_path = Path(manual_dir)
                logger.info(f"使用手动指定目录: {manual_dir}")
            else:
                root_path = Path(root_dir)
                logger.info(f"使用配置的根目录: {root_dir}")

        # 创建路径字典
        paths = {
            "root": root_path,
            "logs": root_path / logs_subdir,
        }

        # 创建所有目录
        for name, path in paths.items():
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"已创建目录: {name} -> {path}")

        logger.info(f"输出目录已初始化，根目录: {root_path}")
        return paths

    def _create_default(self) -> ConfigData:
        """创建默认配置数据.

        :return: 包含默认配置的ConfigData对象
        :rtype: ConfigData
        """
        logger.trace("创建默认配置")
        return ConfigData(
            data=deepcopy(DEFAULT_CONFIG),
            is_valid=True
        )

    def _load_from_file(self, file_path: Union[str, Path]) -> ConfigData:
        """从文件加载配置.

        :param file_path: 配置文件路径
        :type file_path: Union[str, Path]
        :return: 加载的配置数据对象
        :rtype: ConfigData
        :raises FileNotFoundError: 当配置文件不存在时
        :raises json.JSONDecodeError: 当JSON解析失败时
        """
        logger.trace(f"从文件加载配置: {file_path}")
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

            # 验证配置
            errors = ConfigValidator.validate_full_config(loaded_data)
            is_valid = len(errors) == 0

            if not is_valid:
                error_msg = "\n".join(errors)
                logger.warning(f"配置验证失败:\n{error_msg}")

            config_data = ConfigData(
                data=loaded_data,
                file_path=file_path,
                is_valid=is_valid,
                validation_errors=errors
            )

            logger.info(f"成功加载配置文件: {file_path}")
            return config_data

        except json.JSONDecodeError as e:
            logger.opt(exception=e).error(f"JSON解析失败: {e}")
            raise
        except Exception as e:
            logger.opt(exception=e).error("加载配置文件失败")
            raise
