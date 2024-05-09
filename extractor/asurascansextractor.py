from common import Metadata
from extractor.extractor import Extractor
import re
from bs4 import BeautifulSoup

class AsurascansExtractor(Extractor):
  domain = "asuracomic.net"

  def __init__(self, config):
    super().__init__(config)

  def _is_chapter(self, url, resp) -> bool:
    return "-chapter-" in url
  
  def _get_metadata(self, url, resp) -> Metadata:
    soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")
    title_div = soup.find('div', class_="ts-breadcrumb bixbox")
    title_div = title_div.find_all('li', itemprop="itemListElement")[1]
    span_text = title_div.find('span').text
    h1_tag = soup.find('h1', class_='entry-title')
    text = h1_tag.text.strip()

    return Metadata({
        "manga": span_text,
        "chapter": text,
        "chapter_minor": None,
        "lang": "en",
        "language": "English",
    })
  
  def _get_images(self, url, resp) -> list[str]:
    soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")
    div = soup.find('div', class_="rdminimal")
    img_tags = div.find_all('img')
    img_sources = [img['src'] for img in img_tags if 'src' in img.attrs]
    return img_sources