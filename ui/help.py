from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown

class HelpWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel('帮助文档')
        layout.addWidget(label)
        self.web = QWebEngineView()
        help_md = '''\
# 【知识库管理工具帮助】

- **知识库**：支持分类-子标题-知识点三级结构，右键可插入图片/代码/视频，支持Markdown实时预览。
- **日程管理**：支持添加、右键删除、提醒、统计等，界面美观。
- **番茄钟**：支持倒计时、背景自定义、日期显示。
- **设置**：支持主题、字体、字体大小、最小化到托盘等配置。
- **快捷键**：Ctrl+S保存、Ctrl+N新建、Ctrl+Q退出、F11全屏。
- **托盘**：可最小化到系统托盘，托盘菜单可还原主界面。
- **安全**：知识点内容加密存储。

---

**作者：wyt**  
**联系方式：wyt.ybsc@gmail.com**

更多功能详见README。
'''
        html = markdown.markdown(help_md, extensions=['fenced_code', 'tables'])
        self.web.setHtml(f'<html><body style="font-size:15px;">{html}</body></html>')
        layout.addWidget(self.web)

    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()
