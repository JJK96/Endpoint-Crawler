import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Parameter:
    name: str
    type: str

    def __repr__(self):
        return self.type + " " + self.name


@dataclass
class Endpoint:
    request_type: str
    path: str
    file: str
    parameters: list[Parameter]


class BaseCrawler:
    filetypes = []

    def find_relevant_files(self, dir, filetypes):
        for root, dirs, files in os.walk(dir):
            for file in files:
                for filetype in filetypes:
                    if file.endswith("." + filetype):
                        yield Path(root) / file

    def regex_on_file(self, filename, patterns):
        with open(filename) as f:
            contents = f.read()
        for pattern in patterns:
            yield from re.finditer(pattern, contents, flags=re.MULTILINE | re.DOTALL)

    def find_endpoints(self, dir) -> Iterator[Endpoint]:
        for file in self.find_relevant_files(dir, self.filetypes):
            yield from self.find_endpoints_file(file)
