import requests
import os
import ssl
import random
import importlib.util
import binascii
from utils import get_logger
from utils.config import Config
from requests.adapters import HTTPAdapter

# referenced: https://github.com/mikf/gallery-dl/tree/master

class RequestsAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None):
        self.ssl_context = ssl_context
        HTTPAdapter.__init__(self)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return HTTPAdapter.init_poolmanager(self, *args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return HTTPAdapter.proxy_manager_for(self, *args, **kwargs)

class Downloader:
    def __init__(self, config: Config):
        self.session = session = requests.Session()
        self.logger = get_logger(f"Downloader", "DOWNLOADER")
        self.config = config
        self.cookies_domain = ""
        headers = session.headers
        headers.clear()

        self.setup_headers()

    def setup_headers(self):
        """ Configure session headers from INI config file """
        encoding = "gzip, deflate, br" if importlib.util.find_spec("brotli") else "gzip, deflate"

        headers = self.session.headers
        ssl_ciphers = ssl_options = 0

        platform = self.config.PLATFORMS[self.config.platform]
        browser = self.config.browser

        for key, value in self.config.HTTP_HEADERS[browser]:
            if value and "{}" in value:
                headers[key] = value.format(platform)
            else:
                headers[key] = value

        ssl_options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 |
                        ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        ssl_ciphers = self.config.SSL_CIPHERS[browser]

        headers["Accept-Encoding"] = encoding

        adapter = self._build_requests_adapter(ssl_options, ssl_ciphers)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _init_cookies(self):
        pass

    def _build_requests_adapter(self, ssl_options, ssl_ciphers):
        if ssl_options or ssl_ciphers:
            ssl_context = ssl.create_default_context()
            if ssl_options:
                ssl_context.options |= ssl_options
            if ssl_ciphers:
                ssl_context.set_ecdh_curve("prime256v1")
                ssl_context.set_ciphers(ssl_ciphers)
        else:
            ssl_context = None

        adapter = RequestsAdapter(
            ssl_context)
        return adapter
    
    def cookies_store(self):
        """Store the session's cookies in a cookies.txt file"""

        path = self.config.cookie_save

        path_tmp = path + ".tmp"
        try:
            with open(path_tmp, "w") as fp:
                self.cookiestxt_store(fp, self.cookies)
            os.replace(path_tmp, path)
        except OSError as exc:
            self.log.warning("cookies: %s", exc)

    def _prepare_ddosguard_cookies(self):
        if not self.cookies.get("__ddg2", domain=self.cookies_domain):
            self.cookies.set(
                "__ddg2", self.generate_token(), domain=self.cookies_domain)
            
    def generate_token(self, size=16):
        """Generate a random token with hexadecimal digits"""
        data = random.getrandbits(size * 8).to_bytes(size, "big")
        return binascii.hexlify(data).decode()

    def cookiestxt_store(self, fp, cookies):
        """Write 'cookies' in Netscape cookies.txt format to 'fp'"""
        write = fp.write
        write("# Netscape HTTP Cookie File\n\n")

        for cookie in cookies:
            if not cookie.domain:
                continue

            if cookie.value is None:
                name = ""
                value = cookie.name
            else:
                name = cookie.name
                value = cookie.value

            write("\t".join((
                cookie.domain,
                "TRUE" if cookie.domain.startswith(".") else "FALSE",
                cookie.path,
                "TRUE" if cookie.secure else "FALSE",
                "0" if cookie.expires is None else str(cookie.expires),
                name,
                value + "\n",
            )))

    def request(self, url, method="GET"):
        response = None
        try:
            response = self.session.request(method, url)
            code = response.status_code
            server = response.headers.get("Server")
            if server and server.startswith("cloudflare") and \
                    code in (403, 503):
                content = response.content
                if b"_cf_chl_opt" in content or b"jschl-answer" in content:
                    self.logger.error("Cloudflare challenge")
                if b'name="captcha-bypass"' in content:
                    self.logger.error("Cloudflare CAPTCHA")
            return response
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ContentDecodingError) as exc:
            print(exc)
        except (requests.exceptions.RequestException) as exc:
            raise print(exc)

if __name__ == "__main__":
    from configparser import ConfigParser
    from utils.config import Config
    cparser = ConfigParser()
    cparser.read("config.ini")
    config = Config(cparser)
    url = "https://asuracomic.net/1908287720-reaper-of-the-drifting-moon-chapter-86/"
    dl = Downloader(config)
    content = dl.request(url).content
    with open("dump.txt", "w") as fh:
        fh.write(str(content))