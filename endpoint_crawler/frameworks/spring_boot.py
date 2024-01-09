from .base import BaseCrawler, Endpoint
from ..util import Url
from javalang.parse import parse
from javalang.tree import ElementValuePair, ElementArrayValue

class SpringBootCrawler(BaseCrawler):
    filetypes = ["java"]
    mappings = ["GetMapping", "PostMapping", "PutMapping", "DeleteMapping", "PatchMapping"]

    def find_endpoints_file(self, file):
        with open(file) as f:
            tree = parse(f.read())
        for c in tree.types:
            base = None
            for annotation in c.annotations:
                if annotation.name == "RequestMapping":
                    base = Url(annotation.element.values[0].value.strip('"'))
                    break
            if not base:
                continue
            for method in c.methods:
                for annotation in method.annotations:
                    if annotation.name in self.mappings:
                        value = None
                        if isinstance(annotation.element, list):
                            for e in annotation.element: 
                                if isinstance(e, ElementValuePair) and e.name == "value":
                                    value = e.value.values[0].value.strip('"')
                                    break
                        elif isinstance(annotation.element, ElementArrayValue):
                                value = annotation.element.values[0].value.strip('"')
                        if value is None:
                            continue
                        path = base / value
                        request_type = annotation.name.replace("Mapping", "")
                        yield Endpoint(request_type, path, file)
