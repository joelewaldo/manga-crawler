from threading import Thread, RLock
from queue import Queue, Empty

from utils import get_logger, get_urlhash, normalize
from scraper import find
from scraper.scraper import Scraper
from crawler.dbworker import DBWorker

class Frontier(object):
    """
    Manages which url should be grabbed next from the queue and also saves the status of them by keeping track if they have been
    visited or not using a JSON file.
    """

    def __init__(self, config, restart):
        self.logger = get_logger("FRONTIER")
        self.config = config
        self.to_be_downloaded = Queue()
        self.lock = RLock()
        self.db_worker = DBWorker(config.save_file, self.logger)
        self.db_worker.start()

        if restart:
            self.logger.info("Restart flag is set. Clearing the existing database and reinitializing.")
            self.clear_database()
            self.load_seed_urls()
        elif not self.db_worker.db_exists:
            self.logger.info("Database does not exist, but restart is false. Initializing new database with seed URLs.")
            self.load_seed_urls()
        else:
            self.logger.info("Database found. Saved data will be parsed.")
            self.parse_existing_urls()

    def clear_database(self):
        self.db_worker.request("clear_database")

    def load_seed_urls(self):
        """Loads seed URLs into the database and queue."""
        for url in self.config.seed_urls:
            self.add_url(url)
    
    def parse_existing_urls(self):
        """Loads existing URLs from the database that are not completed."""
        urls = self.db_worker.request("get_all_urls")
        total_count = len(urls)
        tbd_count = 0
        for url, completed in urls.values():
            scraper: Scraper = find(url, self.config)
            if not completed and scraper.is_valid(url):
                self.to_be_downloaded.put(url)
                tbd_count += 1
        self.logger.info(f"Found {tbd_count} urls to be downloaded from {total_count} total urls discovered.")

    def get_tbd_url(self):
        """Grabs the next URL to be downloaded from the queue."""
        try:
            return self.to_be_downloaded.get_nowait()
        except Empty:
            return None

    def add_url(self, url):
        with self.lock:
            url = normalize(url)
            urlhash = get_urlhash(url)
            self.db_worker.request("add_url", url, urlhash, False)
            self.to_be_downloaded.put(url)

    def mark_url_complete(self, url):
        with self.lock:
            self.to_be_downloaded.task_done()
            urlhash = get_urlhash(url)
            self.db_worker.request("mark_url_complete", urlhash)

    def __del__(self):
        self.db_worker.stop_worker()
        self.db_worker.join()

