# views/sidebar/sidebar.py
"""侧边栏主组件 - 参照 electerm 风格."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal
from loguru import logger

from .sidebar_button import SidebarButton


class Sidebar(QWidget):
    """侧边栏组件.

    36px 宽的垂直图标栏，参照 electerm 的 sidebar 实现。
    """

    # 信号定义
    menu_clicked = Signal()       # 菜单按钮点击
    add_clicked = Signal()        # 添加按钮点击
    bookmark_clicked = Signal()   # 收藏按钮点击
    settings_clicked = Signal()   # 设置按钮点击
    log_clicked = Signal()        # 日志按钮点击
    about_clicked = Signal()      # 关于按钮点击

    def __init__(self, parent=None):
        """初始化侧边栏.

        :param parent: 父组件
        """
        super().__init__(parent)
        logger.trace("初始化侧边栏")

        self.setFixedWidth(36)
        self.setObjectName("sidebar")

        self._init_ui()

    def _init_ui(self):
        """初始化UI布局.

        图标完全参照 electerm (Ant Design Icons):
        - 菜单: 使用 logo/汉堡菜单图标
        - 添加: PlusCircleOutlined
        - 收藏: BookOutlined
        - 设置: SettingOutlined
        - 日志: FileTextOutlined
        - 关于: InfoCircleOutlined
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 菜单按钮 - electerm 使用 logo，这里用汉堡菜单图标
        self.btn_menu = SidebarButton("menu", "菜单")
        self.btn_menu.clicked.connect(self.menu_clicked.emit)
        layout.addWidget(self.btn_menu)

        # 添加按钮 - PlusCircleOutlined
        self.btn_add = SidebarButton("plus-circle", "添加")
        self.btn_add.clicked.connect(self.add_clicked.emit)
        layout.addWidget(self.btn_add)

        # 收藏按钮 - BookOutlined
        self.btn_bookmark = SidebarButton("book", "收藏")
        self.btn_bookmark.clicked.connect(self.bookmark_clicked.emit)
        layout.addWidget(self.btn_bookmark)

        # 设置按钮 - SettingOutlined
        self.btn_settings = SidebarButton("setting", "设置")
        self.btn_settings.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(self.btn_settings)

        # 日志按钮 - FileTextOutlined
        self.btn_log = SidebarButton("file-text", "日志")
        self.btn_log.clicked.connect(self.log_clicked.emit)
        layout.addWidget(self.btn_log)

        # 关于按钮 - InfoCircleOutlined
        self.btn_about = SidebarButton("info-circle", "关于")
        self.btn_about.clicked.connect(self.about_clicked.emit)
        layout.addWidget(self.btn_about)

        # 弹性空间，将按钮推到顶部
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        logger.trace("侧边栏UI初始化完成")
