# 知识库管理工具

本项目是一个基于 PyQt5 的知识库管理工具，支持知识分类/子标题/知识点三级管理、数据加密、Markdown 编辑与实时预览、插入图片/代码/视频、番茄钟、日程管理、主题/字体/托盘/快捷键/美观UI/帮助页面等功能。

## 技术架构
- **界面**：PyQt5 + Qt Designer
- **富文本/Markdown**：QTextBrowser + QWebEngineView + markdown/pygments
- **数据存储**：sqlite3（本地文件，db/database.py）
- **加密**：cryptography，知识点内容加密存储（core/encryption.py）
- **主题/字体/设置**：core/theme.py + config/settings.json
- **托盘/通知/快捷键**：PyQt5 系统托盘、QShortcut
- **番茄钟/日程/提醒**：core/pomodoro.py、ui/schedule.py
- **导入导出**：支持 Markdown 文件导入导出

## 主要功能
- 分类/子标题/知识点三级结构，持久化存储
- 知识点内容加密，兼容历史明文
- Markdown 编辑与实时预览，插入图片/代码/视频
- 番茄钟、日程管理、提醒
- 主题切换、字体设置、托盘、快捷键
- 数据导入导出、帮助与作者信息

## 目录结构

```ascii
knowledge/
├── main.py                # 程序入口
├── requirements.txt       # 依赖
├── README.md              # 项目说明
├── config/                # 配置与数据库
│   ├── settings.json      # 主题/字体/托盘等设置
│   ├── knowledge.db       # sqlite3数据库
│   └── key.bin            # 加密密钥
├── db/
│   └── database.py        # 数据库操作
├── core/
│   ├── encryption.py      # 加密解密
│   ├── markdown_render.py # Markdown渲染
│   ├── pomodoro.py        # 番茄钟
│   └── theme.py           # 主题/字体
├── static/
│   └── icons/             # 图标资源
│       └── icon.png
└── ui/
    ├── editor.py          # 主编辑器界面
    ├── help.py            # 帮助页面
    ├── main_window.py     # 主窗口
    ├── pomodoro.py        # 番茄钟界面
    ├── schedule.py        # 日程管理
    ├── settings.py        # 设置界面
    └── tray.py            # 托盘功能
```

## 运行环境
- Python 3.9+
- Linux 桌面环境

## 安装依赖
```fish
pip install -r requirements.txt
```

## 启动
```fish
python main.py
```

## 贡献
欢迎提交 issue 和 PR。

## 示例

### 新建知识点
1. 点击左侧“添加分类”或“添加子标题”按钮，创建分类/子标题。
2. 选中分类或子标题，点击“新建知识点”或直接在编辑区输入内容。
3. 输入标题和内容，点击“保存知识点”。

### 加密存储与导入导出
- 所有知识点内容均加密存储，导入/导出支持 Markdown 文件。
- 导入：点击“导入知识点”，选择 Markdown 文件并输入标题。
- 导出：选中知识点，点击“导出知识点”。

### 主题切换
- 在“设置”页可切换浅色/深色主题，界面自动刷新。

### 番茄钟与日程
- “番茄钟”页可设置专注时长，支持通知提醒。
- “日程管理”页可添加、编辑、删除日程。

## 常见问题（FAQ）

**Q: 启动报错缺少依赖？**
A: 请先运行 `pip install -r requirements.txt` 安装依赖。

**Q: 数据丢失/打不开？**
A: 检查 config/knowledge.db 是否存在或被损坏。建议定期备份 config/ 目录。

**Q: 密码/密钥丢失如何恢复？**
A: 若 config/key.bin 丢失，将无法解密历史加密内容。请妥善备份 key.bin。

**Q: 如何自定义主题/字体？**
A: 在“设置”页可切换主题、字体和字号，或手动编辑 config/settings.json。

**Q: 如何迁移/同步数据？**
A: 复制 config/knowledge.db 和 key.bin 到新环境即可。

## 开发说明

- 主窗口入口：main.py，主界面在 ui/main_window.py
- 编辑器核心：ui/editor.py，所有知识点操作均在此实现
- 数据库接口：db/database.py，支持分类/子标题/知识点三级结构
- 加密模块：core/encryption.py，所有知识点内容加密存储
- 主题/设置：core/theme.py + config/settings.json
- UI美化：apply_theme 方法统一切换主题
- 其他功能：ui/schedule.py（日程）、ui/pomodoro.py（番茄钟）、ui/tray.py（托盘）、ui/help.py（帮助）

如需二次开发，建议遵循模块化结构，扩展新功能时优先在 core/ 和 ui/ 目录下新建模块。
