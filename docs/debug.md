## 程序启动后，创建两个标签时，鼠标悬停另一个未选中的标签上时，标签文字会消失
self._color_text_hover = QColor(theme.tab_hover_bg)  # hover 文字用稍亮色
_color_text_hover（悬停时的文字颜色）被错误地设置为 theme.tab_hover_bg（悬停时的背景颜色）。这导致文字颜色和背景颜色相同，文字自然就"消失"了。

例如在 dark 主题下，tab_hover_bg 是 #3c3c3c，悬停背景也是 #3c3c3c，文字就完全看不见了。

修复方法：应该使用 tab_active_text 作为悬停文字颜色（与选中标签文字一致，悬停时文字变亮）。