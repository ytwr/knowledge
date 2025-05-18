from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QSpinBox, QHBoxLayout, QMessageBox, QApplication, QFontComboBox, QCheckBox
from PyQt5.QtGui import QFont
from core.theme import ThemeManager
from core.pomodoro import PomodoroTimer
import json
import os

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        # 主题选择
        layout.addWidget(QLabel('主题设置:'))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['light', 'dark', 'blue', 'green', 'pink'])
        self.theme_combo.setCurrentText(self.theme_manager.theme)
        layout.addWidget(self.theme_combo)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        # 字体选择
        layout.addWidget(QLabel('字体设置:'))
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(self.theme_manager.font))
        layout.addWidget(self.font_combo)
        self.font_combo.currentFontChanged.connect(self.change_font)
        # 字体大小
        layout.addWidget(QLabel('界面字体大小:'))
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 32)
        self.font_spin.setValue(self.theme_manager.font_size)
        layout.addWidget(self.font_spin)
        self.font_spin.valueChanged.connect(self.change_font_size)
        # 编辑器字体大小
        layout.addWidget(QLabel('编辑器字体大小:'))
        self.editor_font_spin = QSpinBox()
        self.editor_font_spin.setRange(8, 32)
        self.editor_font_spin.setValue(self.theme_manager.editor_font_size)
        layout.addWidget(self.editor_font_spin)
        self.editor_font_spin.valueChanged.connect(self.change_editor_font_size)
        # 番茄钟设置
        layout.addWidget(QLabel('番茄钟时长(分钟):'))
        self.pomodoro_spin = QSpinBox()
        self.pomodoro_spin.setRange(10, 120)
        self.pomodoro_spin.setValue(25)
        layout.addWidget(self.pomodoro_spin)
        # 最小化到托盘开关
        self.tray_checkbox = QCheckBox('最小化到系统托盘')
        self.tray_checkbox.setChecked(self.theme_manager.minimize_to_tray)
        layout.addWidget(self.tray_checkbox)
        self.save_btn = QPushButton('保存设置')
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        self.setStyleSheet('QWidget { font-size: 14px; } QPushButton { background: #4F8EF7; color: white; border-radius: 4px; padding: 6px 12px; } QPushButton:hover { background: #357AE8; } QComboBox, QSpinBox, QFontComboBox { border-radius: 4px; border: 1px solid #ccc; padding: 4px; }')

    def change_theme(self, theme):
        self.theme_manager.theme = theme
        app = QApplication.instance()
        if app:
            self.theme_manager.apply(app)

    def change_font(self, font):
        self.theme_manager.font = font.family()
        app = QApplication.instance()
        if app:
            self.theme_manager.apply(app)

    def change_font_size(self, size):
        self.theme_manager.font = self.theme_manager.font
        app = QApplication.instance()
        if app:
            self.theme_manager.apply(app)

    def change_editor_font_size(self, size):
        self.theme_manager.editor_font_size = size
        from ui.editor import EditorWidget
        for w in self.parent().findChildren(EditorWidget):
            w.editor.setFont(QFont(self.theme_manager.font, size))

    def save_settings(self):
        self.theme_manager.theme = self.theme_combo.currentText()
        self.theme_manager.font = self.font_combo.currentFont().family()
        self.theme_manager.font_size = self.font_spin.value()
        self.theme_manager.editor_font_size = self.editor_font_spin.value()
        self.theme_manager.minimize_to_tray = self.tray_checkbox.isChecked()
        self.theme_manager.save()
        QMessageBox.information(self, '设置', '设置已保存')
        # 立即刷新字体
        app = QApplication.instance()
        if app:
            self.theme_manager.apply(app)

    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()
