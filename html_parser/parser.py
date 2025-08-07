from bs4 import BeautifulSoup
from lxml import html
from lxml.etree import tostring
from . import formatter

class HTMLParser:

    def __init__(self, content: str):

        if not isinstance(content, str) or not content:
            raise TypeError("content must be a string")

        self.html_content = content

        self._soup = None
        self._lxml_tree = None

    @property
    def soup(self) -> BeautifulSoup:
        if self._soup is None:
            self._soup = BeautifulSoup(self.html_content, 'lxml')
        return self._soup

    @property
    def lxml_tree(self):
        if self._lxml_tree is None:
            self._lxml_tree = html.fromstring(self.html_content)
        return self._lxml_tree

    def get_metadata(self) -> dict:

        metadata = {}

        title_tag = self.soup.find('title')
        metadata['title'] = title_tag.get_text(strip=True) if title_tag else None

        desc_tag = self.soup.find('meta', attrs={'name': 'description'})
        metadata['description'] = desc_tag['content'] if desc_tag and 'content' in desc_tag.attrs else None

        keywords_tag = self.soup.find('meta', attrs={'name': 'keywords'})
        metadata['keywords'] = keywords_tag['content'] if keywords_tag and 'content' in keywords_tag.attrs else None

        author_tag = self.soup.find('meta', attrs={'name': 'author'})
        metadata['author'] = author_tag['content'] if author_tag and 'content' in author_tag.attrs else None

        return metadata

    def get_text_by_css(self, content_selector: str) -> str:

        content_area = self.soup.select_one(content_selector)

        return formatter.format_to_structured_text(content_area)

    def get_text_by_xpath(self, content_selector: str) -> str:

        content_areas = self.lxml_tree.xpath(content_selector)

        if content_areas:
            lxml_element = content_areas[0]
            html_element = tostring(lxml_element, encoding='unicode')
            soup_tag = BeautifulSoup(html_element, 'lxml').find()
            return formatter.format_to_structured_text(soup_tag)
        return ""

    def parse(self, selector: str, selector_type: str = 'css') -> dict:

        metadata = self.get_metadata()

        if selector_type == 'css':
            structured_text = self.get_text_by_css(selector)
        elif selector_type == 'xpath':
            structured_text = self.get_text_by_xpath(selector)
        else:
            raise ValueError(f"unsupported selector type: {selector_type}")

        return {
            'metadata': metadata,
            'structured_text': structured_text
        }