from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QMenuBar, QAction, QDialog, QMenu
from PyQt5.QtCore import Qt
from ui.editor import EditorWidget
from ui.schedule import ScheduleWidget
from ui.settings import SettingsWidget
from ui.help import HelpWidget
import sys
sys.path.append('./ui')
from ui.pomodoro import PomodoroWidget
from ui.tray import TrayIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from core.theme import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('知识库管理工具')
        self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        # 知识库编辑器
        self.editor_tab = EditorWidget()
        self.tabs.addTab(self.editor_tab, '知识库')
        # 日程管理
        self.schedule_tab = ScheduleWidget()
        self.tabs.addTab(self.schedule_tab, '日程管理')
        # 番茄钟
        self.pomodoro_tab = PomodoroWidget()
        self.tabs.addTab(self.pomodoro_tab, '番茄钟')
        # 设置
        self.settings_tab = SettingsWidget(self)
        self.tabs.addTab(self.settings_tab, '设置')
        # 帮助
        self.help_tab = HelpWidget(self)
        self.tabs.addTab(self.help_tab, '帮助')
        # 托盘功能
        self.theme_manager = ThemeManager()
        self.tray = TrayIcon(self)
        self.tray.show()
        self.tray.show_action.triggered.connect(self.showNormal)
        # 读取设置决定是否启用最小化到托盘
        self.minimize_to_tray = self.theme_manager.__dict__.get('minimize_to_tray', False)
        # 快捷键
        QShortcut(QKeySequence('Ctrl+S'), self, activated=self.save_current)
        QShortcut(QKeySequence('Ctrl+N'), self, activated=self.new_knowledge)
        QShortcut(QKeySequence('Ctrl+Q'), self, activated=self.close)
        QShortcut(QKeySequence('F11'), self, activated=self.toggle_fullscreen)

    def save_current(self):
        # 保存当前Tab内容（如知识库编辑器）
        if self.tabs.currentWidget() and hasattr(self.tabs.currentWidget(), 'save_knowledge'):
            self.tabs.currentWidget().save_knowledge()

    def new_knowledge(self):
        # 新建知识点
        if self.tabs.currentWidget() and hasattr(self.tabs.currentWidget(), 'add_knowledge'):
            self.tabs.currentWidget().add_knowledge()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def closeEvent(self, event):
        if getattr(self, 'minimize_to_tray', False):
            self.hide()
            self.tray.showMessage('知识库管理工具', '程序已最小化到托盘，可在托盘区还原。')
            event.ignore()
        else:
            event.accept()
