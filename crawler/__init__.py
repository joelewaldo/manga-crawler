from utils import get_logger
from utils.download import Downloader
from crawler.frontier import Frontier
from crawler.worker import Worker
from crawler.politeness import Politeness

class Crawler(object):
    """
    initializes the crawler with all the necessary config variables
    """

    def __init__(
        self,
        config,
        restart,
        frontier_factory=Frontier,
        worker_factory=Worker,
        politeness_factory=Politeness,
        downloader_factory=Downloader,
    ):
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory
        self.politeness = politeness_factory(config)
        self.downloader = downloader_factory(config)

    def start_async(self):
        self.workers = [
            self.worker_factory(
                worker_id,
                self.config,
                self.frontier,
                self.politeness,
                self.downloader,
            )
            for worker_id in range(self.config.threads_count)
        ]
        for worker in self.workers:
            worker.start()

    def start(self):
        self.start_async()
        self.join()

    def join(self):
        for worker in self.workers:
            worker.join()