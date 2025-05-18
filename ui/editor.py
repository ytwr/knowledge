from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter, QListWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QInputDialog, QMessageBox, QTextBrowser, QTreeWidget, QTreeWidgetItem, QCheckBox, QFileDialog, QMenu, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
from core.markdown_render import MarkdownRenderer
from core.encryption import encrypt_data, decrypt_data
from db.database import Database

class EditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.renderer = MarkdownRenderer()
        self.db = Database()
        self.init_ui()
        self.apply_theme()  # 初始化时应用主题
        self.load_knowledge_list()

    def init_ui(self):
        layout = QHBoxLayout(self)
        self.splitter = QSplitter()
        # 左侧分类树+搜索
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('搜索知识点...')
        self.search_bar.textChanged.connect(self.search_knowledge)
        left_layout.addWidget(self.search_bar)
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabel('分类/子标题/知识点')
        self.category_tree.itemClicked.connect(self.on_tree_item_clicked)
        left_layout.addWidget(self.category_tree)
        self.add_cat_btn = QPushButton('添加分类')
        self.add_cat_btn.clicked.connect(self.add_category)
        left_layout.addWidget(self.add_cat_btn)
        self.add_sub_btn = QPushButton('添加子标题')
        self.add_sub_btn.clicked.connect(self.add_subtitle)
        left_layout.addWidget(self.add_sub_btn)
        self.splitter.addWidget(left_panel)
        # 中间编辑区
        self.editor_panel = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_panel)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText('知识点标题')
        self.editor_layout.addWidget(self.title_edit)
        self.editor = QTextBrowser()
        self.editor.setOpenExternalLinks(True)
        self.editor.setAcceptRichText(True)
        self.editor.setReadOnly(False)
        self.editor_layout.addWidget(self.editor)
        # 去除多余按钮，只保留必要操作
        # self.save_btn = QPushButton('保存')
        # self.save_btn.clicked.connect(self.save_knowledge)
        # self.editor_layout.addWidget(self.save_btn)
        # Markdown实时预览
        self.preview_checkbox = QCheckBox('显示Markdown实时预览')
        self.preview_checkbox.setChecked(False)
        self.preview_checkbox.stateChanged.connect(self.toggle_preview)
        self.editor_layout.addWidget(self.preview_checkbox)
        self.editor_panel.setLayout(self.editor_layout)
        self.splitter.addWidget(self.editor_panel)
        # 右侧预览区
        self.preview = QWebEngineView()
        self.preview.setVisible(False)
        self.splitter.addWidget(self.preview)
        self.splitter.setSizes([220, 700, 700])
        layout.addWidget(self.splitter)
        self.setLayout(layout)
        self.setStyleSheet('''
            QWidget { font-size: 15px; background: #f5f7fa; }
            QPushButton { background: #4F8EF7; color: white; border-radius: 4px; padding: 7px 16px; }
            QPushButton:hover { background: #357AE8; }
            QLineEdit, QTextEdit, QTextBrowser { border-radius: 4px; border: 1px solid #ccc; padding: 4px; background: #fff; }
            QTreeWidget { border-radius: 4px; border: 1px solid #ccc; }
            QCheckBox { margin: 6px; }
        ''')
        self.editor.textChanged.connect(self.update_preview)
        # 添加导入导出按钮
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton('保存知识点')
        self.save_btn.clicked.connect(self.save_knowledge)
        btn_layout.addWidget(self.save_btn)
        self.import_btn = QPushButton('导入知识点')
        self.import_btn.clicked.connect(self.import_knowledge)
        btn_layout.addWidget(self.import_btn)
        self.export_btn = QPushButton('导出知识点')
        self.export_btn.clicked.connect(self.export_knowledge)
        btn_layout.addWidget(self.export_btn)
        self.editor_layout.addLayout(btn_layout)

    def apply_theme(self, theme_name=None):
        """
        统一应用主题样式，可根据 theme_name 切换不同主题。
        """
        # 可扩展多主题，这里仅示例两种
        if theme_name == 'dark':
            style = '''
                QWidget { font-size: 15px; background: #23272e; color: #e0e0e0; }
                QPushButton { background: #3b4252; color: #e0e0e0; border-radius: 4px; padding: 7px 16px; border: 1px solid #4F8EF7; }
                QPushButton:hover { background: #4F8EF7; color: #fff; }
                QLineEdit, QTextEdit, QTextBrowser { border-radius: 4px; border: 1px solid #444; padding: 4px; background: #2e3440; color: #e0e0e0; }
                QTreeWidget { border-radius: 4px; border: 1px solid #444; background: #2e3440; color: #e0e0e0; }
                QTreeWidget::item:selected { background: #4F8EF7; color: #fff; }
                QCheckBox { margin: 6px; color: #e0e0e0; }
            '''
        else:
            style = '''
                QWidget { font-size: 15px; background: #f5f7fa; color: #222; }
                QPushButton { background: #4F8EF7; color: white; border-radius: 4px; padding: 7px 16px; }
                QPushButton:hover { background: #357AE8; }
                QLineEdit, QTextEdit, QTextBrowser { border-radius: 4px; border: 1px solid #ccc; padding: 4px; background: #fff; color: #222; }
                QTreeWidget { border-radius: 4px; border: 1px solid #ccc; background: #fff; color: #222; }
                QTreeWidget::item:selected { background: #4F8EF7; color: #fff; }
                QCheckBox { margin: 6px; color: #222; }
            '''
        self.setStyleSheet(style)
        # 强制刷新控件
        self.category_tree.viewport().update()
        self.editor.viewport().update()
        self.title_edit.update()
        self.repaint()
        # 可选：切换主题后重新加载数据，防止显示异常
        self.load_knowledge_list()

    def load_knowledge_list(self, selected_cat_id=None, selected_sub_id=None):
        self.category_tree.clear()
        categories = self.db.get_categories()
        for cat_id, cat_name in categories:
            cat_item = QTreeWidgetItem([cat_name])
            cat_item.setData(0, Qt.UserRole, ('category', cat_id))
            subtitles = self.db.get_subtitles(cat_id)
            for sub_id, sub_name in subtitles:
                sub_item = QTreeWidgetItem([sub_name])
                sub_item.setData(0, Qt.UserRole, ('subtitle', sub_id, cat_id))
                knowledges = self.db.get_knowledges(category_id=cat_id, subtitle_id=sub_id)
                for kid, title in knowledges:
                    k_item = QTreeWidgetItem([title])
                    k_item.setData(0, Qt.UserRole, ('knowledge', kid))
                    sub_item.addChild(k_item)
                cat_item.addChild(sub_item)
            self.category_tree.addTopLevelItem(cat_item)
            # 自动展开新加的分类/子标题
            if selected_cat_id and cat_id == selected_cat_id:
                cat_item.setExpanded(True)
                if selected_sub_id:
                    for i in range(cat_item.childCount()):
                        if cat_item.child(i).data(0, Qt.UserRole)[1] == selected_sub_id:
                            cat_item.child(i).setExpanded(True)

    def add_category(self):
        cat, ok = QInputDialog.getText(self, '新建分类', '输入分类名:')
        if ok and cat:
            cat_id = self.db.add_category(cat)
            self.load_knowledge_list(selected_cat_id=cat_id)

    def add_subtitle(self):
        cat_item = self.category_tree.currentItem()
        if cat_item and cat_item.data(0, Qt.UserRole) and cat_item.data(0, Qt.UserRole)[0] == 'category':
            cat_id = cat_item.data(0, Qt.UserRole)[1]
            subtitle, ok = QInputDialog.getText(self, '新建子标题', '输入子标题名:')
            if ok and subtitle:
                sub_id = self.db.add_subtitle(subtitle, cat_id)
                self.load_knowledge_list(selected_cat_id=cat_id, selected_sub_id=sub_id)

    def add_knowledge(self):
        item = self.category_tree.currentItem()
        cat_id = sub_id = None
        if item:
            data = item.data(0, Qt.UserRole)
            if data[0] == 'category':
                cat_id = data[1]
            elif data[0] == 'subtitle':
                sub_id = data[1]
                cat_id = data[2]
        title, ok = QInputDialog.getText(self, '新建知识点', '输入标题:')
        if ok and title and cat_id:
            enc_content = encrypt_data('')  # 修复：去除.decode('utf-8')
            kid = self.db.add_knowledge(title, cat_id, sub_id, enc_content, encrypted=1)
            self.load_knowledge_list(selected_cat_id=cat_id, selected_sub_id=sub_id)

    def on_tree_item_clicked(self, item, col):
        data = item.data(0, Qt.UserRole)
        if data and data[0] == 'knowledge':
            kid = data[1]
            row = self.db.get_knowledge(kid)
            if row:
                _, title, content, encrypted = row
                # 路径显示：类别/子标题/知识点标题
                parent = item.parent()
                if parent:
                    sub_name = parent.text(0)
                    cat_name = parent.parent().text(0) if parent.parent() else ''
                else:
                    sub_name = ''
                    cat_name = ''
                # 只显示知识点标题，便于编辑
                self.title_edit.setText(title)
                self.title_edit.setReadOnly(False)
                if encrypted:
                    try:
                        # 兼容历史数据：如果content不是base64字符串，直接显示原文
                        import base64
                        try:
                            # 检查是否为base64字符串
                            base64.b64decode(content)
                            content = decrypt_data(content)
                        except Exception:
                            pass  # 不是base64密文，直接显示
                    except Exception:
                        content = '[解密失败]'
                self.editor.setHtml(content)
                self.current_kid = kid
                self.current_cat = cat_name
                self.current_sub = sub_name
                # 实时预览
                if self.preview_checkbox.isChecked():
                    text = self.editor.toPlainText()
                    html = self.renderer.render(text)
                    self.preview.setHtml(html)
        else:
            self.title_edit.clear()
            self.title_edit.setReadOnly(False)
            self.editor.clear()
            self.current_kid = None
            self.current_cat = None
            self.current_sub = None
            self.preview.setHtml('')

    # 右键菜单支持重命名/删除分类和子标题
    def contextMenuEvent(self, event):
        item = self.category_tree.itemAt(self.category_tree.viewport().mapFromGlobal(event.globalPos()))
        if not item:
            return
        data = item.data(0, Qt.UserRole)
        menu = QMenu(self)
        if data:
            if data[0] == 'category':
                rename_action = QAction('重命名分类', self)
                rename_action.triggered.connect(lambda: self.rename_category(item))
                del_action = QAction('删除分类', self)
                del_action.triggered.connect(lambda: self.delete_category(item))
                menu.addAction(rename_action)
                menu.addAction(del_action)
            elif data[0] == 'subtitle':
                rename_action = QAction('重命名子标题', self)
                rename_action.triggered.connect(lambda: self.rename_subtitle(item))
                del_action = QAction('删除子标题', self)
                del_action.triggered.connect(lambda: self.delete_subtitle(item))
                menu.addAction(rename_action)
                menu.addAction(del_action)
        menu.exec_(event.globalPos())

    def rename_category(self, item):
        cat_id = item.data(0, Qt.UserRole)[1]
        new_name, ok = QInputDialog.getText(self, '重命名分类', '新分类名:')
        if ok and new_name:
            self.db.rename_category(cat_id, new_name)
            self.load_knowledge_list(selected_cat_id=cat_id)

    def delete_category(self, item):
        cat_id = item.data(0, Qt.UserRole)[1]
        reply = QMessageBox.question(self, '删除分类', '确定要删除该分类及其下所有内容吗？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_category(cat_id)
            self.load_knowledge_list()

    def rename_subtitle(self, item):
        sub_id = item.data(0, Qt.UserRole)[1]
        new_name, ok = QInputDialog.getText(self, '重命名子标题', '新子标题名:')
        if ok and new_name:
            self.db.rename_subtitle(sub_id, new_name)
            cat_id = item.data(0, Qt.UserRole)[2]
            self.load_knowledge_list(selected_cat_id=cat_id, selected_sub_id=sub_id)

    def delete_subtitle(self, item):
        sub_id = item.data(0, Qt.UserRole)[1]
        cat_id = item.data(0, Qt.UserRole)[2]
        reply = QMessageBox.question(self, '删除子标题', '确定要删除该子标题及其下所有知识点吗？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_subtitle(sub_id)
            self.load_knowledge_list(selected_cat_id=cat_id)

    def search_knowledge(self, text):
        self.category_tree.clear()
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM knowledge WHERE title LIKE ? OR content LIKE ?', (f'%{text}%', f'%{text}%'))
        for cat_row in cursor.fetchall():
            cat = cat_row[0] or '未分类'
            cat_item = QTreeWidgetItem([cat])
            cursor.execute('SELECT id, title FROM knowledge WHERE category=? AND (title LIKE ? OR content LIKE ?)', (cat, f'%{text}%', f'%{text}%'))
            for row in cursor.fetchall():
                kid, title = row
                item = QTreeWidgetItem([title])
                item.setData(0, 1, kid)
                cat_item.addChild(item)
            self.category_tree.addTopLevelItem(cat_item)

    def update_preview(self):
        if self.preview_checkbox.isChecked():
            text = self.editor.toPlainText()
            html = self.renderer.render(text)
            self.preview.setHtml(html)

    def toggle_preview(self, state):
        self.preview.setVisible(bool(state))
        if state:
            self.splitter.setSizes([220, 500, 500])
            self.update_preview()
        else:
            self.splitter.setSizes([220, 1000, 0])
            self.preview.setHtml('')

    def show_context_menu(self, pos):
        menu = self.editor.createStandardContextMenu()
        menu.addSeparator()
        img_action = QAction('插入图片', self)
        img_action.triggered.connect(self.insert_image)
        menu.addAction(img_action)
        code_action = QAction('插入代码', self)
        code_action.triggered.connect(self.insert_code)
        menu.addAction(code_action)
        video_action = QAction('插入视频', self)
        video_action.triggered.connect(self.insert_video)
        menu.addAction(video_action)
        menu.exec_(self.editor.mapToGlobal(pos))

    def insert_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Images (*.png *.jpg *.bmp *.jpeg *.gif)')
        if fname:
            html = f'<img src="file://{fname}" style="max-width:100%;" />'
            cursor = self.editor.textCursor()
            cursor.insertHtml(html)

    def insert_code(self):
        code, ok = QInputDialog.getMultiLineText(self, '插入代码', '输入代码:')
        if ok and code:
            html = f'<pre style="background:#232629;color:#eee;padding:8px;border-radius:4px;"><code>{code}</code></pre>'
            cursor = self.editor.textCursor()
            cursor.insertHtml(html)

    def insert_video(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择视频', '', 'Videos (*.mp4 *.webm *.ogg)')
        if fname:
            html = f'<video src="file://{fname}" controls style="max-width:100%;"></video>'
            cursor = self.editor.textCursor()
            cursor.insertHtml(html)

    def save_knowledge(self):
        # 允许新建/编辑知识点时，自动用文本框标题或内容第一行作为标题
        item = self.category_tree.currentItem()
        # 获取父路径（分类/子标题）
        cat_id = sub_id = None
        cat_name = sub_name = None
        if item:
            data = item.data(0, Qt.UserRole)
            # 选中知识点时，父节点为子标题或分类
            if data and data[0] == 'knowledge':
                parent = item.parent()
                if parent:
                    sub_name = parent.text(0)
                    cat_name = parent.parent().text(0) if parent.parent() else ''
                else:
                    sub_name = ''
                    cat_name = ''
            elif data and data[0] == 'subtitle':
                sub_name = item.text(0)
                cat_name = item.parent().text(0) if item.parent() else ''
            elif data and data[0] == 'category':
                cat_name = item.text(0)
        # 查找cat_id和sub_id
        for cid, cname in self.db.get_categories():
            if cname == cat_name:
                cat_id = cid
                break
        if sub_name:
            for sid, sname in self.db.get_subtitles(cat_id):
                if sname == sub_name:
                    sub_id = sid
                    break
        # 获取标题：优先用标题输入框，否则用内容第一行
        title = self.title_edit.text().strip()
        if not title:
            content_plain = self.editor.toPlainText().strip()
            title = content_plain.split('\n', 1)[0] if content_plain else ''
        if not title or not cat_id:
            QMessageBox.warning(self, '保存失败', '知识点标题和分类不能为空')
            return
        content = self.editor.toHtml()
        enc_content = encrypt_data(content)  # 已是str，无需decode
        # 判断是更新还是新建
        if hasattr(self, 'current_kid') and self.current_kid:
            self.db.update_knowledge(self.current_kid, title, enc_content, encrypted=1)
        else:
            self.db.add_knowledge(title, cat_id, sub_id, enc_content, encrypted=1)
        self.load_knowledge_list(selected_cat_id=cat_id, selected_sub_id=sub_id)
        QMessageBox.information(self, '保存成功', '知识点内容已加密保存')
        self.title_edit.setText(title)
        self.current_cat = cat_name
        self.current_sub = sub_name

    def export_knowledge(self):
        from PyQt5.QtWidgets import QFileDialog
        item = self.category_tree.currentItem()
        if not item:
            QMessageBox.warning(self, '未选择', '请先选择一个知识点')
            return
        data = item.data(0, Qt.UserRole)
        if not data or data[0] != 'knowledge':
            QMessageBox.warning(self, '未选择', '请先选择一个知识点')
            return
        kid = data[1]
        row = self.db.get_knowledge(kid)
        if not row:
            QMessageBox.warning(self, '错误', '知识点不存在')
            return
        _, title, content, encrypted = row
        if encrypted:
            try:
                content = decrypt_data(content)
            except Exception:
                content = '[解密失败]'
        fname, _ = QFileDialog.getSaveFileName(self, '导出知识点', f'{title}.md', 'Markdown Files (*.md);;All Files (*)')
        if fname:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, '导出成功', f'已导出到 {fname}')

    def import_knowledge(self):
        from PyQt5.QtWidgets import QFileDialog
        item = self.category_tree.currentItem()
        cat_id = sub_id = None
        if item:
            data = item.data(0, Qt.UserRole)
            if data[0] == 'category':
                cat_id = data[1]
            elif data[0] == 'subtitle':
                sub_id = data[1]
                cat_id = data[2]
        if not cat_id:
            QMessageBox.warning(self, '未选择', '请先选择一个分类或子标题')
            return
        fname, _ = QFileDialog.getOpenFileName(self, '导入知识点', '', 'Markdown Files (*.md);;All Files (*)')
        if fname:
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
            title, ok = QInputDialog.getText(self, '知识点标题', '输入知识点标题:')
            if ok and title:
                enc_content = encrypt_data(content)  # 已是str，无需decode
                self.db.add_knowledge(title, cat_id, sub_id, enc_content, encrypted=1)
                self.load_knowledge_list(selected_cat_id=cat_id, selected_sub_id=sub_id)
                QMessageBox.information(self, '导入成功', f'已导入知识点“{title}”')
