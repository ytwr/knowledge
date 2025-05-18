# Markdown渲染与代码高亮模块
import markdown
from pygments.formatters import HtmlFormatter

class MarkdownRenderer:
    def __init__(self):
        self.md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
        self.formatter = HtmlFormatter(style='default')

    def render(self, text):
        html = self.md.reset().convert(text)
        style = f'<style>{self.formatter.get_style_defs()}</style>'
        return style + html
