from abc import ABC, abstractmethod
from urllib.parse import urlparse

class Scraper(ABC):
    def __init__(self, url, config):
        self.config = config
        self.url = url

    def find_links(self, url, resp) -> list[str]:
        links = self.extract_next_links(url, resp)
        res = [link for link in links if self.is_valid(link)]
        return res
    
    def is_relative(self, url):
        """
        returns whether or not the url is a relative url
        """
        return not urlparse(url).netloc

    @abstractmethod
    def extract_next_links(self, url, resp) -> list[str]:
        """
        Subclass must implement this method
        """
        pass

    @abstractmethod
    def is_valid(self, url) -> bool:
        """
        Subclass must implement this method
        """
        pass