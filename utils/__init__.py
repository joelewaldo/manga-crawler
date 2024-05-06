import os
import logging
from hashlib import sha256
from urllib.parse import urlparse


def get_logger(name, filename=None):
    logger = logging.getLogger(name)
    if not hasattr(logger, 'handler_set') or not logger.handler_set:
        logger.setLevel(logging.INFO)
        log_dir = "Logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if filename is None:
            filename = name
        file_path = os.path.join(log_dir, f"{filename}.log")

        fh = logging.FileHandler(file_path)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        logger.handler_set = True

    return logger


def get_urlhash(url):
    parsed = urlparse(url)
    # everything other than scheme.
    return sha256(
        f"{parsed.netloc}/{parsed.path}/{parsed.params}/"
        f"{parsed.query}/{parsed.fragment}".encode("utf-8")
    ).hexdigest()


def normalize(url):
    if url.endswith("/"):
        return url.rstrip("/")
    return url

def getBaseUrl(url):
        """Extract the base URL from the given URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"