# 主题与字体配置模块
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/settings.json')

DEFAULT_THEME = 'light'
DEFAULT_FONT = '微软雅黑'
DEFAULT_FONT_SIZE = 15
DEFAULT_EDITOR_FONT_SIZE = 15
DEFAULT_MINIMIZE_TO_TRAY = False

def ensure_default_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        default = {
            'theme': DEFAULT_THEME,
            'font': DEFAULT_FONT,
            'font_size': DEFAULT_FONT_SIZE,
            'editor_font_size': DEFAULT_EDITOR_FONT_SIZE,
            'minimize_to_tray': DEFAULT_MINIMIZE_TO_TRAY
        }
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(default, f)

class ThemeManager:
    def __init__(self):
        ensure_default_config()
        self.theme = DEFAULT_THEME
        self.font = DEFAULT_FONT
        self.font_size = DEFAULT_FONT_SIZE
        self.editor_font_size = DEFAULT_EDITOR_FONT_SIZE
        self.minimize_to_tray = DEFAULT_MINIMIZE_TO_TRAY
        self.load()

    def load(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.theme = data.get('theme', DEFAULT_THEME)
                self.font = data.get('font', DEFAULT_FONT)
                self.font_size = data.get('font_size', DEFAULT_FONT_SIZE)
                self.editor_font_size = data.get('editor_font_size', DEFAULT_EDITOR_FONT_SIZE)
                self.minimize_to_tray = data.get('minimize_to_tray', DEFAULT_MINIMIZE_TO_TRAY)

    def apply(self, app: QApplication):
        # 主题切换可扩展
        if self.theme == 'dark':
            app.setStyleSheet('QWidget { background: #232629; color: #eee; }')
        else:
            app.setStyleSheet('')
        app.setFont(QFont(self.font, self.font_size))

    def save(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({'theme': self.theme, 'font': self.font, 'font_size': self.font_size, 'editor_font_size': self.editor_font_size, 'minimize_to_tray': self.minimize_to_tray}, f)
