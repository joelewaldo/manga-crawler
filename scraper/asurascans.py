from scraper.scraper import Scraper
from extractor import find
from extractor.extractor import Extractor
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re

class Asurascans(Scraper):
    domain = "asuracomic.net"

    def __init__(self, url, config):
        super().__init__(url, config)
    
    def extract_next_links(self, url, resp) -> list[str]:
        extractor: Extractor = find(url, self.config)
        extractor.extract(url, resp)

        soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")
        links = []

        # finds all the anchor tags and href links and turns them all into absolute urls
        all_links = soup.find_all("a")
        for link in all_links:
            href = link.get("href")
            if href:
                if self.is_relative(href):
                    href = urljoin(url, href)
                links.append(href)
        return links
    
    def is_valid(self, url) -> bool:
        try:
            parsed = urlparse(url)

            if parsed.scheme not in set(["http", "https"]):
                return False
            
            domain = parsed.netloc

            if not self.domain == domain:
                return False

            return not re.match(
                r".*\.(css|js|bmp|gif|ico"
                + r"|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|war"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|ppsx"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$",
                parsed.path.lower(),
            )

        except TypeError:
            print("TypeError for ", parsed)
            raise

    def __repr__(self):
        return f"TcbScraper(url={self.url})"