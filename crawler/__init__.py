from utils import get_logger
from utils.download import Downloader
from crawler.frontier import Frontier
from crawler.worker import Worker
from crawler.politeness import Politeness

import signal
import sys

class Crawler:
    def __init__(self, config, restart):
        self.logger = get_logger("CRAWLER")
        self.config = config
        self.frontier = Frontier(config, restart)
        self.workers = []
        self.politeness = Politeness(config)
        self.downloader = Downloader(config)

    def start_async(self):
        for worker_id in range(self.config.threads_count):
            worker = Worker(worker_id, self.config, self.frontier, self.politeness, self.downloader)
            self.workers.append(worker)
            worker.start()

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.start_async()
        self.join()

    def join(self):
        try:
            for worker in self.workers:
                worker.join()
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt caught, stopping workers.")
            self.stop()

    def stop(self):
        self.logger.info("Stopping the crawler.")
        self.frontier.db_worker.stop_worker()
        for worker in self.workers:
            if worker.is_alive():
                self.logger.info(f"Stopping {worker.name}")

    def signal_handler(self, sig, frame):
        print("SIGINT received. Shutting down the crawler gracefully.")
        self.stop()
        sys.exit(0)