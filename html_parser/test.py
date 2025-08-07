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

        <!-- 新增表格 -->
        <table id="price-table" border="1">
            <caption>价格表</caption>
            <thead>
                <tr>
                    <th>产品</th>
                    <th>价格（元）</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>苹果</td>
                    <td>5.00</td>
                </tr>
                <tr>
                    <td>香蕉</td>
                    <td>3.50</td>
                </tr>
            </tbody>
        </table>

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

result_css = parser.parse("#content", "css")
print("metadata:", result_css['metadata'])
print("-------------text----------")
print(result_css["structured_text"])
print("---------------------------")

result_xpath = parser.parse("//main[@id='content']", "xpath")
print("metadata:", result_xpath['metadata'])
print("-------------text----------")
print(result_xpath["structured_text"])
