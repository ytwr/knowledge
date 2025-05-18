# 数据库管理模块
# 负责sqlite3数据库的初始化、连接、基本操作
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../config/knowledge.db')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # 分类表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )''')
        # 子标题表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS subtitle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            UNIQUE(name, category_id),
            FOREIGN KEY(category_id) REFERENCES category(id) ON DELETE CASCADE
        )''')
        # 知识点表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category_id INTEGER,
            subtitle_id INTEGER,
            content TEXT,
            tags TEXT,
            encrypted INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(category_id) REFERENCES category(id) ON DELETE SET NULL,
            FOREIGN KEY(subtitle_id) REFERENCES subtitle(id) ON DELETE SET NULL
        )''')
        # 日程表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            start_time TEXT,
            end_time TEXT,
            remind_time TEXT,
            remind_type TEXT DEFAULT '提前1小时',
            notified INTEGER DEFAULT 0,
            finished INTEGER DEFAULT 0
        )''')
        # 专注记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS focus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER
        )''')
        # 用户设置表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )''')
        self.conn.commit()

    # 分类操作
    def add_category(self, name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO category (name) VALUES (?)', (name,))
        self.conn.commit()
        return cursor.lastrowid

    def get_categories(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name FROM category ORDER BY id')
        return cursor.fetchall()

    def rename_category(self, cat_id, new_name):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE category SET name=? WHERE id=?', (new_name, cat_id))
        self.conn.commit()

    def delete_category(self, cat_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM category WHERE id=?', (cat_id,))
        self.conn.commit()

    # 子标题操作
    def add_subtitle(self, name, category_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO subtitle (name, category_id) VALUES (?, ?)', (name, category_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_subtitles(self, category_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name FROM subtitle WHERE category_id=? ORDER BY id', (category_id,))
        return cursor.fetchall()

    def rename_subtitle(self, sub_id, new_name):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE subtitle SET name=? WHERE id=?', (new_name, sub_id))
        self.conn.commit()

    def delete_subtitle(self, sub_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM subtitle WHERE id=?', (sub_id,))
        self.conn.commit()

    # 知识点操作（部分示例，后续可迁移完善）
    def add_knowledge(self, title, category_id, subtitle_id, content, tags='', encrypted=0):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO knowledge (title, category_id, subtitle_id, content, tags, encrypted, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, datetime("now"), datetime("now"))',
            (title, category_id, subtitle_id, content, tags, encrypted))
        self.conn.commit()
        return cursor.lastrowid

    def get_knowledges(self, category_id=None, subtitle_id=None):
        cursor = self.conn.cursor()
        if category_id and subtitle_id:
            cursor.execute('SELECT id, title FROM knowledge WHERE category_id=? AND subtitle_id=?', (category_id, subtitle_id))
        elif category_id:
            cursor.execute('SELECT id, title FROM knowledge WHERE category_id=?', (category_id,))
        else:
            cursor.execute('SELECT id, title FROM knowledge', ())
        return cursor.fetchall()

    def get_knowledge(self, kid):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, content, encrypted FROM knowledge WHERE id=?', (kid,))
        return cursor.fetchone()

    def update_knowledge(self, kid, title, content, encrypted=1):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE knowledge SET title=?, content=?, encrypted=?, updated_at=datetime("now") WHERE id=?', (title, content, encrypted, kid))
        self.conn.commit()

    def delete_knowledge(self, kid):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM knowledge WHERE id=?', (kid,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def delete_schedule(self, schedule_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM schedule WHERE id=?', (schedule_id,))
        self.conn.commit()
