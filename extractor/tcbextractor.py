from common import Metadata
from extractor.extractor import Extractor
import re
from bs4 import BeautifulSoup

class TcbExtractor(Extractor):
  domain = "tcb-backup.bihar-mirchi.com"

  def __init__(self, config):
    super().__init__(config)

  def _is_chapter(self, url, resp) -> bool:
    return "/chapters/" in url
  
  def _get_metadata(self, url, resp) -> Metadata:
    soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")
    h1_tag = soup.find('h1', class_='text-lg md:text-2xl font-bold mt-8')
    text = h1_tag.text.strip()

    match = re.match(r'^(.*?) - Chapter (\d+)(?:\.(\d+))?$', text)
    manga_title, chapter_major, chapter_minor = match.groups()
    return Metadata({
      "manga": manga_title,
      "chapter": chapter_major,
      "chapter_minor": chapter_minor,
      "lang": "en",
      "language": "English",
    })
  
  def _get_images(self, url, resp) -> list[str]:
    soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")
    img_tags = soup.find_all('img', class_='fixed-ratio-content')
    img_sources = [img['src'] for img in img_tags if 'src' in img.attrs]
    return img_sources