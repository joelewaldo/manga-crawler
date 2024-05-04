from threading import Thread
from crawler.frontier import Frontier
from crawler.politeness import Politeness

from utils.config import Config

from utils.download import Downloader
from utils import get_logger

from scraper import find
from scraper.scraper import Scraper

class Worker(Thread):
    def __init__(self, worker_id, config: Config, frontier: Frontier, politeness: Politeness, downloader: Downloader):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.politeness = politeness
        self.downloader = downloader

        super().__init__(daemon=True)

    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                print("++++++++ (worker.py) The frontier is empty and there were no tbd urls")
                break

            self.politeness.wait_polite(tbd_url)

            # downloads the page
            resp = self.downloader.request(tbd_url)

            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status_code}>."
            )

            scraper: Scraper = find(tbd_url, self.config)

            scraped_urls = scraper.find_links(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)