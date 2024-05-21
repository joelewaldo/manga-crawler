from common import Metadata
from extractor.extractor import Extractor
import re
from bs4 import BeautifulSoup

class RagnarokscansExtractor(Extractor):
  domain = "ragnarokscanlation.org"

  def __init__(self, config):
    super().__init__(config)

  def _is_chapter(self, url, resp) -> bool:
    return "/chapter-" in url
  
  def _get_metadata(self, url, resp) -> Metadata:
    soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")
    heading = soup.find('h1', id='chapter-heading').text
    series_name, chapter_info = heading.split(' - ')
    chapter_number = chapter_info.split()[-1]

    return Metadata({
        "manga": series_name,
        "chapter": chapter_number,
        "chapter_minor": None,
        "lang": "en",
        "language": "English",
    })
  
  def _get_images(self, url, resp) -> list[str]:
    soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")
    page_break_divs = soup.find_all('div', class_='page-break')
    img_sources = [div.find('img')['data-src'] for div in page_break_divs]
    return img_sources