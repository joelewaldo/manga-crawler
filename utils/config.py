class Config(object):
    """
    This class defines all the config parameters used in the program.
    """

    def __init__(self, config):
        self.browser = config["REQUESTS"]["BROWSER"]
        self.platform = config["REQUESTS"]["PLATFORM"]
        self.cookie_save = config["REQUESTS"]["COOKIESAVE"]

        self.threads_count = int(config["LOCAL PROPERTIES"]["THREADCOUNT"])
        self.save_file = config["LOCAL PROPERTIES"]["SAVE"]
        self.manga_dir = config["LOCAL PROPERTIES"]["MANGADIR"]

        self.seed_urls = config["CRAWLER"]["SEEDURL"].split(",")
        self.time_delay = float(config["CRAWLER"]["POLITENESS"])

        self.PLATFORMS = {
        'windows': "Windows NT 10.0; Win64; x64",
        'linux': "X11; Linux x86_64",
        'macos': "Macintosh; Intel Mac OS X 10_15_7"
        }

        self.SSL_CIPHERS = {
            "firefox": (
                "TLS_AES_128_GCM_SHA256:"
                "TLS_CHACHA20_POLY1305_SHA256:"
                "TLS_AES_256_GCM_SHA384:"
                "ECDHE-ECDSA-AES128-GCM-SHA256:"
                "ECDHE-RSA-AES128-GCM-SHA256:"
                "ECDHE-ECDSA-CHACHA20-POLY1305:"
                "ECDHE-RSA-CHACHA20-POLY1305:"
                "ECDHE-ECDSA-AES256-GCM-SHA384:"
                "ECDHE-RSA-AES256-GCM-SHA384:"
                "ECDHE-ECDSA-AES256-SHA:"
                "ECDHE-ECDSA-AES128-SHA:"
                "ECDHE-RSA-AES128-SHA:"
                "ECDHE-RSA-AES256-SHA:"
                "AES128-GCM-SHA256:"
                "AES256-GCM-SHA384:"
                "AES128-SHA:"
                "AES256-SHA"
            ),
            "chrome": (
                "TLS_AES_128_GCM_SHA256:"
                "TLS_AES_256_GCM_SHA384:"
                "TLS_CHACHA20_POLY1305_SHA256:"
                "ECDHE-ECDSA-AES128-GCM-SHA256:"
                "ECDHE-RSA-AES128-GCM-SHA256:"
                "ECDHE-ECDSA-AES256-GCM-SHA384:"
                "ECDHE-RSA-AES256-GCM-SHA384:"
                "ECDHE-ECDSA-CHACHA20-POLY1305:"
                "ECDHE-RSA-CHACHA20-POLY1305:"
                "ECDHE-RSA-AES128-SHA:"
                "ECDHE-RSA-AES256-SHA:"
                "AES128-GCM-SHA256:"
                "AES256-GCM-SHA384:"
                "AES128-SHA:"
                "AES256-SHA"
            ),
        }
        
        self.HTTP_HEADERS = {
            "firefox": (
                ("User-Agent", "Mozilla/5.0 ({}; "
                            "rv:109.0) Gecko/20100101 Firefox/115.0"),
                ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,"
                        "image/avif,image/webp,*/*;q=0.8"),
                ("Accept-Language", "en-US,en;q=0.5"),
                ("Accept-Encoding", None),
                ("Referer", None),
                ("DNT", "1"),
                ("Connection", "keep-alive"),
                ("Upgrade-Insecure-Requests", "1"),
                ("Cookie", None),
                ("Sec-Fetch-Dest", "empty"),
                ("Sec-Fetch-Mode", "no-cors"),
                ("Sec-Fetch-Site", "same-origin"),
                ("TE", "trailers"),
            ),
            "chrome": (
                ("Connection", "keep-alive"),
                ("Upgrade-Insecure-Requests", "1"),
                ("User-Agent", "Mozilla/5.0 ({}) AppleWebKit/537.36 (KHTML, "
                            "like Gecko) Chrome/111.0.0.0 Safari/537.36"),
                ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,"
                        "image/avif,image/webp,image/apng,*/*;q=0.8,"
                        "application/signed-exchange;v=b3;q=0.7"),
                ("Referer", None),
                ("Sec-Fetch-Site", "same-origin"),
                ("Sec-Fetch-Mode", "no-cors"),
                ("Sec-Fetch-Dest", "empty"),
                ("Accept-Encoding", None),
                ("Accept-Language", "en-US,en;q=0.9"),
                ("cookie", None),
                ("content-length", None),
            ),
        }