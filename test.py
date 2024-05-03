from urllib.parse import urlparse, urljoin
import re

domain = "comick.io"

def is_valid(url) -> bool:
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False
        
        ddomain = parsed.netloc

        if not ddomain == domain:
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|ico"
            + r"|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|war"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|ppsx"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$",
            parsed.path.lower(),
        )

    except TypeError:
        print("TypeError for ", parsed)
        raise
    
if __name__ == "__main__":
    print(is_valid("https://comick.io/comic/kaiju-no-8"))