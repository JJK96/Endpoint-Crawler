from .base import BaseCrawler, Endpoint
from urllib.parse import urljoin

class SpringBootCrawler(BaseCrawler):
    filetypes = ["java"]
    patterns = [
        r"@(Get|Post|Put|Delete|Patch)Mapping\([^\)]*?value\s*=\s*{\"([^\"]+)\"}[^\)]*\)",
        r"@(Get|Post|Put|Delete|Patch)Mapping\({\"([^}]+)\"}\)",
    ]
    base_pattern = r"@RequestMapping\({\"([^}]+)\"}\)"

    def find_endpoints_file(self, file):
        base = ""
        done = set()
        for match in self.regex_on_file(file, [self.base_pattern]):
            if match.group(0).startswith("@RequestMapping"):
                base = match.group(1)
                assert base is not None
                break

        for match in self.regex_on_file(file, self.patterns):
            request_type = match.group(1)
            value = match.group(2)
            path = urljoin(base + '/', value)
            key = (request_type, path)
            if key not in done:
                yield Endpoint(request_type, path, file)
                done.add(key)
