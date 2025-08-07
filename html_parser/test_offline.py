from html_parser.parser import HTMLParser

html = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>综合测试页面</title>
    <meta name="description" content="一个用于测试HTML解析器所有功能的页面。">
    
    <style>
        body { font-family: sans-serif; }
        .important { color: red; }
    </style>
    
    <noscript>这段内容在禁用脚本时显示，也应该被移除。</noscript>
</head>
<body>

    <header>
        <h1>网站Logo和顶部广告</h1>
        <p>这里是一些不应出现在最终文本里的内容。</p>
    </header>

    <nav>
        <ul>
            <li><a href="#">首页</a></li>
            <li><a href="#">关于</a></li>
        </ul>
    </nav>

    <main id="main-content">
        <h1>文章主标题 (H1)</h1>
        
        <p>这是文章的第一个段落。它介绍了解析器的基本概念，并且包含一个 <span>span 标签</span> 来测试递归处理。</p>
        
        <h2>一个二级标题 (H2)</h2>

        <p>这是第二个段落，跟在二级标题后面。</p>
        
        <img src="image1.jpg" alt="一只可爱的猫咪" style="width:100px;">
        <img src="image2.jpg" alt=""> <div>
            这是一段直接放在 div 里的文本，用于测试 NavigableString 的处理。
        </div>

        <h4>一个四级标题 (H4)，用来测试不同的标题等级</h4>

        <table>
            <caption>每月开销 | 预算表</caption>
            <thead>
                <tr>
                    <th>项目</th>
                    <th>类型</th>
                    <th>预算 (元)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>餐饮</td>
                    <td>食物 | 饮品</td>
                    <td>1500</td>
                </tr>
                <tr>
                    <td>交通</td>
                    <td>公交 | 地铁</td>
                    <td>200</td>
                </tr>
            </tbody>
        </table>

        <p>下面是列表的例子。</p>

        <h3>无序列表</h3>
        <ul>
            <li>列表项 A</li>
            <li>列表项 B</li>
            <li>列表项 C</li>
        </ul>

        <h3>有序列表</h3>
        <ol>
            <li>第一步</li>
            <li>第二步</li>
            <li>第三步</li>
        </ol>
        
        <iframe src="ads.html" style="display:none;"></iframe>
    </main>
    
    <footer>
        <p>版权所有 &copy; 2025</p>
        <svg height="100" width="100">
            <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
        </svg> 
    </footer>
    
    <script>
        console.log("这段脚本不应该被执行或出现在文本中。");
    </script>
</body>
</html>
"""

parser = HTMLParser(html)

result_css = parser.parse()
# print("metadata:", result_css['metadata'])
# print("-------------text----------")
print(result_css["structured_text"])
print("---------------------------")

# result_xpath = parser.parse("//main[@id='content']", "xpath")
# print("metadata:", result_xpath['metadata'])
# print("-------------text----------")
# print(result_xpath["structured_text"])