from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QColor
from PyQt5.QtCore import Qt, QDate
from core.pomodoro import PomodoroTimer

class PomodoroDial(QWidget):
    def __init__(self, duration=25*60, parent=None):
        super().__init__(parent)
        self.duration = duration
        self.remaining = duration
        self.setMinimumSize(220, 220)
        self.setMaximumSize(300, 300)
        self.setFont(QFont('Arial', 16))

    def set_remaining(self, remaining):
        self.remaining = remaining
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        painter.setRenderHint(QPainter.Antialiasing)
        # 背景
        painter.setBrush(QColor('#f5f5f5'))
        painter.drawEllipse(rect)
        # 进度
        angle = 360 * (self.remaining / self.duration)
        painter.setBrush(QColor('#4F8EF7'))
        painter.drawPie(rect, 90*16, -angle*16)
        # 时间文本
        mins, secs = divmod(self.remaining, 60)
        text = f'{mins:02d}:{secs:02d}'
        painter.setPen(QColor('#232629'))
        painter.setFont(QFont('Arial', 32, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, text)
        # 日期
        painter.setFont(QFont('Arial', 14))
        date_str = QDate.currentDate().toString('yyyy-MM-dd')
        painter.drawText(rect.adjusted(0, 60, 0, 0), Qt.AlignHCenter, date_str)

class PomodoroWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = PomodoroTimer()
        layout = QVBoxLayout(self)
        # 日期显示
        self.date_label = QLabel(QDate.currentDate().toString('yyyy-MM-dd'))
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setFont(QFont('Arial', 18, QFont.Bold))
        layout.addWidget(self.date_label)
        # 时间显示
        self.time_label = QLabel('25:00')
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Arial', 48, QFont.Bold))
        layout.addWidget(self.time_label)
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton('开始')
        self.start_btn.clicked.connect(self.start)
        btn_layout.addWidget(self.start_btn)
        self.stop_btn = QPushButton('停止')
        self.stop_btn.clicked.connect(self.stop)
        btn_layout.addWidget(self.stop_btn)
        self.bg_btn = QPushButton('设置背景图片')
        self.bg_btn.clicked.connect(self.set_bg)
        btn_layout.addWidget(self.bg_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.setStyleSheet('''
            QWidget { font-size: 18px; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f5f7fa, stop:1 #e3e9f3); }
            QLabel { color: #232629; }
            QPushButton { background: #4F8EF7; color: white; border-radius: 4px; padding: 10px 22px; }
            QPushButton:hover { background: #357AE8; }
        ''')
        self.timer.tick.connect(self.update_time)
        self.timer.finished.connect(self.on_finish)
        self.update_time(self.timer.duration)

    def update_time(self, remaining):
        mins, secs = divmod(remaining, 60)
        self.time_label.setText(f'{mins:02d}:{secs:02d}')

    def start(self):
        self.timer.start()
        self.update_time(self.timer.duration)

    def stop(self):
        self.timer.stop()
        self.update_time(self.timer.duration)

    def on_finish(self):
        self.update_time(0)

    def set_bg(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择背景图片', '', 'Images (*.png *.jpg *.bmp)')
        if fname:
            palette = QPalette()
            pixmap = QPixmap(fname)
            palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
