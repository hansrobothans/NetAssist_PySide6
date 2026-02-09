# views/tabs/__init__.py
"""Views标签页模块.

此模块提供各个功能标签页的实现。
"""


from .log_tab import LogTab
from .placeholder_tab import PlaceholderTab

__all__ = [
    "LogTab",
    "PlaceholderTab",
]