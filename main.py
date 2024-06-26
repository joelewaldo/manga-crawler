from argparse import ArgumentParser
from configparser import ConfigParser
from utils.config import Config
from crawler import Crawler

def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    crawler = Crawler(config, restart)
    crawler.start()

if __name__ == "__main__":
   parser = ArgumentParser()
   parser.add_argument("--restart", action="store_true", default=False)
   parser.add_argument("--config_file", type=str, default="config.ini")
   args = parser.parse_args()
   main(args.config_file, args.restart)