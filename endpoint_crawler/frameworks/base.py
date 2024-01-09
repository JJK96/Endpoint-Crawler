import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Endpoint:
    request_type: str
    path: str
    file: str


class BaseCrawler:
    def find_endpoints(self, dir) -> Iterator[Endpoint]:
        raise NotImplemented()

    def find_relevant_files(self, dir, filetypes):
        for root, dirs, files in os.walk(dir):
            for file in files:
                for filetype in filetypes:
                    if file.endswith(filetype):
                        yield Path(root) / file

    def regex_on_file(self, filename, patterns):
        with open(filename) as f:
            contents = f.read()
        for pattern in patterns:
            yield from re.finditer(pattern, contents, flags=re.MULTILINE | re.DOTALL)

