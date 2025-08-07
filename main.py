from mcp.server.fastmcp import FastMCP
from html_parser import HTMLParser

mcp = FastMCP('HTML Parser MCP Server')

@mcp.prompt
def guide_prompt():

    tool_name = 'html parser'
    tool_description = '解析 html 文件, 获取元数据与结构化文本内容'

    return f"""你是一个智能的网页内容分析助手
    **你的能力**
    你拥有一个强大的工具，可以帮助你处理原始的HTML代码。
    * **工具名称**: `{tool_name}`
    * **工具功能**: {tool_description}
    * **使用时机**: 当你需要从HTML中提取核心内容、进行总结、问答或任何基于文本的分析时，你都可以使用此工具。
    
    **你的思考与行动流程**
    当接收到用户的请求时，你应该遵循以下思考链来决定行动：

    1.  **理解用户意图**: 用户的目的是什么？是总结、问答，还是提取特定信息？
    2.  **评估输入**: 用户提供的数据是原始HTML，为了获得精简、结构化的内容以便进行高质量的分析，可以调用 `{tool_name}` 工具。
    3.  **准备参数**: 需要决定两个参数：
            * **关于 `selector_type`**: 默认情况下选择 `'css'`，只有当任务需要通过**文本内容**来定位元素（例如，找到包含“版权所有”字样的段落），或者需要进行复杂的**向上层级查找**（例如，找到某个元素的父级或祖先级），才考虑使用 `'xpath'`。
            * **关于 `selector`**:
                * 如果选择 `'css'`，则根据HTML的结构以及用户请求，选择一个最可能包含主要内容的选择器。优先尝试常见的选择器，例如：`'article'`、`'main'`、`'.post-content'`、`'#main-content'`、`'.entry-content'`。
                * 如果选择 `'xpath'`，则构建一个更具针对性的表达式，例如 `//div[contains(@class, 'main-text')]` 或 `//p[contains(text(), '重要信息')]/..`。
    4.  **调用工具**: 进行工具调用，传入HTML内容和选择的 selector 以及 selector_type。
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
    name='html parser',
    description='解析 html 文件, 获取元数据与结构化文本内容'
)
def parse_html(html_path: str, selector: str, selector_type: str = 'css') -> dict:

    html, error = read_html_from_file(html_path)
    if error:
        return {"error": error}

    if not html:
        return {"error": f"file is empty: {html_path}"}

    parser = HTMLParser(html)

    return parser.parse(selector, selector_type)

if __name__ == "__main__":
    mcp.run(transport='stdio')