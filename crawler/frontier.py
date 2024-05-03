import os
import json
from threading import Thread, RLock
from queue import Queue, Empty

from utils import get_logger, get_urlhash, normalize
from scraper import find
from scraper.extractor import Extractor

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
        self.save_file = self.config.save_file

        # Check existence of the JSON save file
        if not os.path.exists(self.save_file) and not restart:
            self.logger.info(f"Did not find save file {self.save_file}, starting from seed.")
        elif os.path.exists(self.save_file) and restart:
            self.logger.info(f"Found save file {self.save_file}, deleting it.")
            os.remove(self.save_file)

        self.urls = self._load_save_file() if not restart else {}
        if restart or not self.urls:
            for url in self.config.seed_urls:
                self.add_url(url)
        else:
            self._parse_save_file()

    def _load_save_file(self):
        """Loads the state from the JSON save file."""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as file:
                return json.load(file)
        return {}

    def _save_urls(self):
        """Saves the current state to the JSON save file."""
        with self.lock:
            with open(self.save_file, 'w') as file:
                json.dump(self.urls, file, indent=4)

    def _parse_save_file(self):
        """Parses URLs from the save file to be downloaded if they haven't been completed."""
        total_count = len(self.urls)
        tbd_count = 0
        for hashed_url in self.urls:
            url = self.urls[hashed_url]["url"]
            completed = self.urls[hashed_url]["completed"]
            extractor: Extractor = find(url)
            if not completed and extractor.is_valid(url):
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
        """Adds a URL to the queue and saves it in the save file."""
        with self.lock:
            url = normalize(url)
            urlhash = get_urlhash(url)
            if urlhash not in self.urls:
                self.urls[urlhash] = {'url': url, 'completed': False}
                self._save_urls()
                self.to_be_downloaded.put(url)

    def mark_url_complete(self, url):
        """Marks a URL as completed and updates it in the save file."""
        with self.lock:
            self.to_be_downloaded.task_done()
            urlhash = get_urlhash(url)
            if urlhash not in self.urls:
                self.logger.error(f"Completed URL {url}, but have not seen it before.")
            self.urls[urlhash]['completed'] = True
            self._save_urls()

    def __del__(self):
        self._save_urls()

