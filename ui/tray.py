# 系统托盘与通知模块
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
import os

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        # 设置托盘图标，优先使用项目内的icon.png
        icon_path = os.path.join(os.path.dirname(__file__), '../static/icons/icon.png')
        if not os.path.exists(icon_path):
            icon = QIcon.fromTheme('application-exit')  # 兜底用系统图标
        else:
            icon = QIcon(icon_path)
        super().__init__(icon, parent)
        self.setToolTip('知识库管理工具')
        self.menu = QMenu()
        self.show_action = QAction('显示主界面')
        self.quit_action = QAction('退出')
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.quit_action)
        self.setContextMenu(self.menu)
        self.quit_action.triggered.connect(QCoreApplication.quit)
