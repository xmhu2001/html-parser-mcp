from bs4 import BeautifulSoup
from . import formatter

class HTMLParser:

    def __init__(self, content: str):

        if not isinstance(content, str) or not content:
            raise TypeError("content must be a string")

        self.soup = BeautifulSoup(content, 'lxml')

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


    def get_structured_text(self, content_selector: str) -> str:

        content_area = self.soup.select_one(content_selector)

        return formatter.format_to_structured_text(content_area)

    def parse(self, content_selector: str) -> dict:

        metadata = self.get_metadata()
        structured_text = self.get_structured_text(content_selector)

        return {
            'metadata': metadata,
            'structured_text': structured_text
        }