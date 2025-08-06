from bs4 import Tag, Comment, NavigableString
import re

def clean_html_tree(tag: Tag):
    """
    从给定的BeautifulSoup标签中移除不必要的元素
    """
    noise_tag = ['script', 'style', 'noscript', 'iframe', 'svg', 'header', 'nav', 'footer']

    for t in tag.find_all(noise_tag):
        t.decompose()

    for c in tag.find_all(string=lambda text: isinstance(text, Comment)):
        c.extract()

def format_to_structured_text(tag: Tag) -> str:
    """
    将BeautifulSoup标签及其内容转换为保留结构的纯文本
    - 标题 (h1-h6) 会被加上Markdown风格的前缀 (#)
    - 列表 (ul, ol, li) 会被格式化
    - 段落 (p) 会被保留并用换行符分隔
    """
    if not isinstance(tag, Tag):
        return ""

    clean_html_tree(tag)

    text_parts = []

    for element in tag.descendants:
        if isinstance(element, NavigableString):
            parent_name = element.parent.name
            text = element.strip()
            if text and parent_name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']:
                if element.parent.name not in ['html', 'body', 'div', 'span', 'a']:
                    text_parts.append(text + ' ')

        elif isinstance(element, Tag):
            if element.name in [f'h{i}' for i in range(1, 7)]:
                prefix = '#' * int(element.name[1])
                text_parts.append(f"\n{prefix} {element.get_text(strip=True)}\n\n")
            elif element.name == 'p':
                text_parts.append(element.get_text(strip=True) + "\n\n")
            elif element.name == 'li':
                text_parts.append(f"* {element.get_text(strip=True)}\n")
            elif element.name in ['ul', 'ol']:
                text_parts.append("\n")

    full_text = "".join(text_parts)

    cleaned_text = re.sub(r'\n{3,}', '\n\n', full_text)
    return cleaned_text.strip()

