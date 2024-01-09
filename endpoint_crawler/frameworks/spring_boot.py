from .base import BaseCrawler, Endpoint

class SpringBootCrawler(BaseCrawler):
    filetypes = ["java"]
    patterns = [
        r"@(Get|Post|Put|Delete|Patch)Mapping\([^\)]*?value\s*=\s*{\"([^\"]+)\"}[^\)]*\)",
        r"@(Get|Post|Put|Delete|Patch|Request)Mapping\({\"([^}]+)\"}\)",
    ]

    def find_endpoints(self, dir):
        base = ""
        for file in self.find_relevant_files(dir, self.filetypes):
            for match in self.regex_on_file(file, self.patterns):
                if match.group(0).startswith("@RequestMapping"):
                    base = match.group(2)
                    assert base is not None
                else:
                    request_type = match.group(1)
                    value = match.group(2)
                    path = base + value
                    yield Endpoint(request_type, path)
