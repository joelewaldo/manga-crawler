from abc import ABC, abstractmethod
from common import Metadata
from PIL import Image
from utils import get_logger
from io import BytesIO
from pathlib import Path
from utils.config import Config
from utils.download import Downloader
from requests.exceptions import HTTPError

class Extractor(ABC):

  def __init__(self, config: Config):
    self.config = config
    self.downloader = Downloader(config)
    self.logger = get_logger("Extractor", "Extractor")

  def extract(self, url, resp) -> None:
    if self._is_chapter(url, resp):
      self.logger.info(f"Trying to extract images from: {url}")
      data = self._get_metadata(url, resp)
      images = self._get_images(url, resp)
      self._compile(images, data)

  def _compile(self, images: list[str], metadata: Metadata) -> None:
    chapter_tag = metadata.chapter if not metadata.chapter_minor else str(metadata.chapter) + "-" + str(metadata.chapter_minor)
    directory_path = Path(f"{self.config.manga_dir}/{metadata.manga}")
    directory_path.mkdir(parents=True, exist_ok=True)

    image_files = []
    for image_url in images:
        try:  
          response = self.downloader.request(image_url)
          response.raise_for_status()
        except HTTPError as err:
          self.logger.error(f"Failed to extract an image. Reason: {err}.\n"
                            "Skipping image...")
          continue
        img = Image.open(BytesIO(response.content))
        image_files.append(img)

    pdf_path = directory_path / f"{metadata.manga}-{metadata.chapter}.pdf"
    if image_files:
        image_files[0].save(pdf_path, save_all=True, append_images=image_files[1:], format='PDF')

    pdf_path = directory_path / f"{metadata.manga}-{chapter_tag}.pdf"
    image_files[0].save(pdf_path, save_all=True, append_images=image_files[1:])
    self.logger.info(f"Successfully saved: {pdf_path}")

  @abstractmethod
  def _is_chapter(self, url, resp) -> bool:
    pass

  @abstractmethod
  def _get_metadata(self, url, resp) -> Metadata:
    pass 

  @abstractmethod
  def _get_images(self, url, resp) -> list[str]:
    pass