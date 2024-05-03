from utils.download import Downloader
from configparser import ConfigParser
from utils.config import Config

def main(config_file):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)

    dl = Downloader(config)
    response = dl.request("https://comick.io/home")
    print(response.content)

if __name__ == "__main__":
    main("config.ini")