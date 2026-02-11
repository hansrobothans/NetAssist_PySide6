## 程序启动后，创建两个标签时，鼠标悬停另一个未选中的标签上时，标签文字会消失
self._color_text_hover = QColor(theme.tab_hover_bg)  # hover 文字用稍亮色
_color_text_hover（悬停时的文字颜色）被错误地设置为 theme.tab_hover_bg（悬停时的背景颜色）。这导致文字颜色和背景颜色相同，文字自然就"消失"了。

例如在 dark 主题下，tab_hover_bg 是 #3c3c3c，悬停背景也是 #3c3c3c，文字就完全看不见了。

修复方法：应该使用 tab_active_text 作为悬停文字颜色（与选中标签文字一致，悬停时文字变亮）。

## 标签栏，拖动标签，字体会消失，只有×会显示出来问题
setTabsClosable(False) — 不再让 Qt 创建关闭按钮 widget
_paint_tab 中自绘 × 按钮（两条交叉线），悬停时高亮
_close_btn_rect() 辅助方法计算 × 区域
mousePressEvent 检测 × 点击，发射 tabCloseRequested
mouseMoveEvent 追踪 × 悬停状态
这样所有标签内容（徽章、图标、文字、×）都在 paintEvent 中统一绘制，拖拽时自然跟随移动。