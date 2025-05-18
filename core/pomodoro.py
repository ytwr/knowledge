# 专注与番茄钟模块
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
import time

class PomodoroTimer(QObject):
    tick = pyqtSignal(int)  # 剩余秒数
    finished = pyqtSignal()

    def __init__(self, duration=25*60):
        super().__init__()
        self.duration = duration
        self.remaining = duration
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)

    def start(self):
        self.remaining = self.duration
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def reset(self, duration=None):
        if duration:
            self.duration = duration
        self.remaining = self.duration
        self.timer.stop()

    def is_running(self):
        return self.timer.isActive()

    def _on_tick(self):
        self.remaining -= 1
        self.tick.emit(self.remaining)
        if self.remaining <= 0:
            self.timer.stop()
            self.finished.emit()
