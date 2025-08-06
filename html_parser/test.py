from html_parser.parser import HTMLParser

html = """
<!doctype html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <title>示例页面</title>
    <meta name="description" content="这是描述">
    <meta name="keywords" content="测试,BeautifulSoup">
    <meta name="author" content="张三">
</head>
<body>
    <header>顶部导航</header>
    <main id="content">
        <h1>主标题</h1>
        <p>第一段正文。</p>
        <ul>
            <li>列表项 1</li>
            <li>列表项 2</li>
        </ul>
        <p>第二段正文。</p>
    </main>
    <footer>页脚</footer>
</body>
</html>
"""

parser = HTMLParser(html)
result = parser.parse("#content")      # 用 CSS 选择器定位正文区域
print("metadata:", result['metadata'])
print("text:\n", result['structured_text'])