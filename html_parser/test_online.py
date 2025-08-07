from html_parser.parser import HTMLParser
import requests

url = "https://www.runoob.com/html/html-tutorial.html"

def fetch_html_from_url(url: str) -> tuple[str | None, str | None]:
    """从URL获取并解码网页内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        return response.text, None

    except requests.exceptions.RequestException as e:
        return None, f"network error: {e}"


html, _ = fetch_html_from_url(url)
print(html)
parser = HTMLParser(html)

result_css = parser.parse()
# print("metadata:", result_css['metadata'])
print("-------------text----------")
print(result_css["structured_text"])

