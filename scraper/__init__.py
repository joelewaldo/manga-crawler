import sys
import os
from urllib.parse import urlparse
import importlib

module_directory = './scraper'
if module_directory not in sys.path:
    sys.path.append(module_directory)

module_domains = {
    "comick": "comick.io",
    "tcb": "tcb-backup.bihar-mirchi.com",
    "asurascans": "asuracomic.net",
    "ragnarokscans": "ragnarokscanlation.org"
}

def _list_classes():
    """Dynamically import modules and collect classes with a 'domain' attribute."""
    class_list = []
    for module_name in module_domains:
        module = importlib.import_module(module_name)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and hasattr(attribute, 'domain'):
                class_list.append(attribute)
    return class_list

def find(url, config):
    """Find a suitable scraper for the given URL by checking the domain."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    for cls in _list_classes():
        if domain == cls.domain:
            return cls(url, config)
    return None

if __name__ == "__main__":
    url = "https://comick.io/home"
    scraper = find(url)
    if scraper:
        print(f"Scraper found: {scraper}")
    else:
        print("No suitable scraper found.")