from bs4 import Tag, Comment, NavigableString
import re

def _clean_html_tree(tag: Tag):
    """
    从给定的BeautifulSoup标签中移除不必要的元素
    """
    noise_tag = ['script', 'style', 'noscript', 'iframe', 'svg', 'header', 'nav', 'footer']

    for t in tag.find_all(noise_tag):
        t.decompose()

    for c in tag.find_all(string=lambda text: isinstance(text, Comment)):
        c.extract()


def _format_table_to_markdown(table_tag: Tag) -> str:
    """
    将代表<table>的BeautifulSoup Tag对象转换为Markdown表格格式
    """
    if not isinstance(table_tag, Tag) or table_tag.name != 'table':
        return ""

    markdown_lines = []

    rows = table_tag.find_all('tr')

    for i, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])

        cell_texts = [cell.get_text(strip=True).replace('|', r'\|') for cell in cells]

        markdown_row = '| ' + ' | '.join(cell_texts) + ' |'
        markdown_lines.append(markdown_row)

        if i == 0:
            separator = '|' + '|'.join(['---'] * len(cells)) + '|'
            markdown_lines.append(separator)

    return '\n'.join(markdown_lines)

def _recursive_format(tag: Tag) -> str:
    """
    将BeautifulSoup标签及其内容转换为保留结构的纯文本
    """
    text_parts = []

    for child in tag.children:
        if isinstance(child, NavigableString):
            text = child.strip()
            if text:
                text_parts.append(text + " ")

        elif isinstance(child, Tag):
            if child.name == 'table':
                markdown_table = _format_table_to_markdown(child)
                text_parts.append(markdown_table + "\n\n")

            elif child.name in [f'h{i}' for i in range(1, 7)]:
                prefix = '#' * int(child.name[1])
                text_parts.append(f"\n{prefix} {child.get_text(strip=True)}\n\n")

            elif child.name == 'p':
                text_parts.append(child.get_text(strip=True) + "\n\n")

            elif child.name == 'img':
                alt_text = child.get('alt', '').strip()
                if alt_text:
                    text_parts.append(f"[picture desc: {alt_text}]\n")

            elif child.name == 'li':
                text_parts.append(f"* {child.get_text(strip=True)}\n")

            elif child.name in ['ul', 'ol']:
                text_parts.append("\n" + _recursive_format(child) + "\n")

            else:
                text_parts.append(_recursive_format(child))

    return "".join(text_parts)

def format_to_structured_text(tag: Tag) -> str:

    if not isinstance(tag, Tag):
        return ""

    _clean_html_tree(tag)

    full_text = _recursive_format(tag)

    cleaned_text = re.sub(r'\n{3,}', '\n\n', full_text)

    return cleaned_text.strip()

