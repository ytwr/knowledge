from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QDateTimeEdit, QTextEdit, QInputDialog, QMessageBox, QDialog, QFormLayout, QLineEdit, QCalendarWidget, QComboBox, QMenu, QAction
from PyQt5.QtCore import QDateTime, QTimer, QDateTime as QDT, Qt, QPropertyAnimation
import datetime
from db.database import Database

class ScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('新建日程')
        layout = QFormLayout(self)
        self.title_edit = QLineEdit()
        layout.addRow('标题:', self.title_edit)
        self.start_datetime = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_datetime.setDisplayFormat('yyyy-MM-dd HH:mm')
        self.start_datetime.setCalendarPopup(True)
        layout.addRow('开始时间:', self.start_datetime)
        self.end_datetime = QDateTimeEdit(QDateTime.currentDateTime().addSecs(3600))
        self.end_datetime.setDisplayFormat('yyyy-MM-dd HH:mm')
        self.end_datetime.setCalendarPopup(True)
        layout.addRow('结束时间:', self.end_datetime)
        self.remind_combo = QComboBox()
        self.remind_combo.addItems(['提前1小时', '提前2小时', '提前3小时', '提前6小时', '提前12小时', '提前24小时'])
        layout.addRow('提醒方式:', self.remind_combo)
        self.desc_edit = QTextEdit()
        layout.addRow('描述:', self.desc_edit)
        self.ok_btn = QPushButton('确定')
        self.ok_btn.clicked.connect(self.accept)
        layout.addRow(self.ok_btn)

    def get_data(self):
        return (
            self.title_edit.text(),
            self.start_datetime.dateTime().toString('yyyy-MM-dd HH:mm'),
            self.end_datetime.dateTime().toString('yyyy-MM-dd HH:mm'),
            self.remind_combo.currentText(),
            self.desc_edit.toPlainText()
        )

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        self.load_schedule_list()
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(60 * 1000)  # 每分钟检查一次

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.on_calendar_select)
        layout.addWidget(self.calendar)
        stat_layout = QHBoxLayout()
        self.month_btn = QPushButton('本月统计')
        self.month_btn.clicked.connect(self.month_stats)
        stat_layout.addWidget(self.month_btn)
        self.week_btn = QPushButton('本周统计')
        self.week_btn.clicked.connect(self.week_stats)
        stat_layout.addWidget(self.week_btn)
        layout.addLayout(stat_layout)
        self.add_btn = QPushButton('添加日程')
        self.add_btn.clicked.connect(self.add_schedule)
        layout.addWidget(self.add_btn)
        self.del_btn = QPushButton('删除所选日程')
        self.del_btn.clicked.connect(self.delete_selected_schedule)
        layout.addWidget(self.del_btn)
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.show_schedule)
        layout.addWidget(self.list_widget)
        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        layout.addWidget(self.detail)
        self.setStyleSheet('''
            QWidget { font-size: 15px; background: #f5f7fa; }
            QPushButton { background: #4F8EF7; color: white; border-radius: 4px; padding: 7px 16px; }
            QPushButton:hover { background: #357AE8; }
            QListWidget { border-radius: 4px; border: 1px solid #ccc; }
            QCalendarWidget QAbstractItemView { selection-background-color: #4F8EF7; }
            QTextEdit { background: #fff; border-radius: 4px; border: 1px solid #ccc; }
        ''')
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_list_context_menu)

    def on_calendar_select(self):
        date = self.calendar.selectedDate().toString('yyyy-MM-dd')
        self.list_widget.clear()
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT id, title, remind_time FROM schedule WHERE remind_time LIKE ? ORDER BY remind_time DESC', (f'{date}%',))
        for row in cursor.fetchall():
            self.list_widget.addItem(f'{row[0]}: {row[1]} - {row[2]}')

    def load_schedule_list(self):
        # 默认加载今天的日程
        self.on_calendar_select()

    def add_schedule(self):
        dialog = ScheduleDialog(self)
        if dialog.exec_():
            title, start_time, end_time, remind_type, desc = dialog.get_data()
            if not title or not start_time or not end_time:
                QMessageBox.warning(self, '输入不完整', '标题和时间不能为空')
                return
            cursor = self.db.conn.cursor()
            cursor.execute('INSERT INTO schedule (title, description, start_time, end_time, remind_time, remind_type) VALUES (?, ?, ?, ?, ?, ?)',
                (title, desc, start_time, end_time, start_time, remind_type))
            self.db.conn.commit()
            self.load_schedule_list()

    def delete_selected_schedule(self):
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, '未选择', '请先选择一个日程')
            return
        sid = int(item.text().split(':')[0])
        reply = QMessageBox.question(self, '确认删除', '确定要删除该日程吗？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_schedule(sid)
            self.load_schedule_list()
            self.detail.clear()

    def show_schedule(self, item):
        sid = int(item.text().split(':')[0])
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT title, description, start_time, end_time, remind_type FROM schedule WHERE id=?', (sid,))
        row = cursor.fetchone()
        if row:
            # 动画效果：高亮显示详情区
            self.detail.setPlainText(f'标题: {row[0]}\n开始: {row[2]}\n结束: {row[3]}\n提醒: {row[4]}\n描述:\n{row[1]}')
            anim = QPropertyAnimation(self.detail, b"windowOpacity")
            anim.setDuration(400)
            anim.setStartValue(0.3)
            anim.setEndValue(1.0)
            anim.start()
            self._anim = anim  # 防止动画被回收

    def month_stats(self):
        # 统计本月每天日程数
        from collections import Counter
        cursor = self.db.conn.cursor()
        month = self.calendar.selectedDate().toString('yyyy-MM')
        cursor.execute('SELECT remind_time FROM schedule WHERE remind_time LIKE ?', (f'{month}%',))
        days = [r[0][8:10] for r in cursor.fetchall()]
        count = Counter(days)
        msg = '\n'.join([f'{month}-{d}: {count[d]} 个日程' for d in sorted(count)])
        QMessageBox.information(self, '本月统计', msg or '本月无日程')

    def week_stats(self):
        # 统计本周每天日程数
        from collections import Counter
        import datetime
        cursor = self.db.conn.cursor()
        today = self.calendar.selectedDate().toPyDate()
        start = today - datetime.timedelta(days=today.weekday())
        end = start + datetime.timedelta(days=6)
        cursor.execute('SELECT remind_time FROM schedule WHERE remind_time BETWEEN ? AND ?', (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))
        days = [r[0][8:10] for r in cursor.fetchall()]
        count = Counter(days)
        msg = '\n'.join([f"{start.strftime('%Y-%m')}-{d}: {count[d]} 个日程" for d in sorted(count)])
        QMessageBox.information(self, '本周统计', msg or '本周无日程')

    def check_reminders(self):
        now = QDT.currentDateTime().toString('yyyy-MM-dd HH:mm')
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT id, title, remind_time, remind_type, finished FROM schedule WHERE finished=0')
        for sid, title, remind_time, remind_type, finished in cursor.fetchall():
            # 计算提醒时间
            remind_delta = int(remind_type.replace('提前','').replace('小时',''))
            remind_dt = datetime.datetime.strptime(remind_time, '%Y-%m-%d %H:%M') - datetime.timedelta(hours=remind_delta)
            now_dt = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M')
            if remind_dt <= now_dt < remind_dt + datetime.timedelta(minutes=1):
                QMessageBox.information(self, '日程提醒', f'日程“{title}”即将开始！')
            # 未结束的日程每隔1小时提醒
            if not finished:
                start_dt = datetime.datetime.strptime(remind_time, '%Y-%m-%d %H:%M')
                end_dt = datetime.datetime.strptime(self.get_end_time(sid), '%Y-%m-%d %H:%M')
                if start_dt <= now_dt < end_dt and now_dt.minute == 0:
                    QMessageBox.information(self, '日程提醒', f'日程“{title}”正在进行中，请注意进度！')

    def get_end_time(self, sid):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT end_time FROM schedule WHERE id=?', (sid,))
        row = cursor.fetchone()
        return row[0] if row else ''

    def show_list_context_menu(self, pos):
        item = self.list_widget.itemAt(pos)
        if item:
            menu = QMenu(self)
            del_action = QAction('删除日程', self)
            del_action.triggered.connect(lambda: self.delete_selected_schedule())
            menu.addAction(del_action)
            menu.exec_(self.list_widget.mapToGlobal(pos))