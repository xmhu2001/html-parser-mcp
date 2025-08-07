from mcp.server.fastmcp import FastMCP
from html_parser import HTMLParser

mcp = FastMCP('HTML Parser MCP Server')

@mcp.prompt()
def guide_prompt():

    return f"""你是一个HTML文件内容分析助手
    **能力**
    你拥有一个强大的工具，可以帮助你处理原始的HTML代码。
    * **工具名称**: html_parser
    * **工具功能**: 解析 html 文件, 获取元数据与结构化文本内容。特别地，图片的 ALT 文本被解析为"[picture desc:]"形式的文本，当查找到此格式的内容即判定为图片的 ALT 文本。
    
    **你的思考与行动流程**
    当接收到用户的请求时，你应该遵循以下思考链来决定行动：
    1.  **理解用户意图**: 用户的目的是什么，是总结、问答，还是提取特定信息？
    2.  **准备参数并调用工具**: 
        * 若用户输入中没有明确说明使用的 selector，工具调用时仅传入HTML文件路径，不传入 selector 和 selector_type
        * 若用户输入中明确给定 selector 和 selector_type 的值（例如指定 selector 为"#main-content"），则工具调用时使用提供的 selector 和 selector_type
        * 否则工具调用时仅传入HTML文件路径，不传入 selector 和 selector_type
    """

def read_html_from_file(file_path: str) -> tuple[str | None, str | None]:
    """从本地文件中读取HTML内容并返回一个字符串。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read(), None
    except FileNotFoundError:
        error_msg = f"错误：文件未找到。路径：'{file_path}'"
        return None, error_msg
    except Exception as e:
        error_msg = f"读取文件时发生未知错误: {e}"
        return None, error_msg

@mcp.tool(
    name='html_parser',
    description='解析 html 文件, 获取元数据与结构化文本内容'
)
def parse_html(html_path: str, selector: str | None = None, selector_type: str = 'css') -> dict:

    html, error = read_html_from_file(html_path)
    if error:
        return {"error": error}

    if not html:
        return {"error": f"file is empty: {html_path}"}

    parser = HTMLParser(html)

    return parser.parse(selector, selector_type)

if __name__ == "__main__":
    mcp.run(transport='stdio')