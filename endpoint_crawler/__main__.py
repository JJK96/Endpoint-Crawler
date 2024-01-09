import click
import csv
import sys
from . import find_endpoints
from .util import Url

@click.command()
@click.option("--dir", default=".", help="Directory to search in")
@click.option("--base-url", default="", help="Base URL for the application")
@click.option("--framework", default="spring_boot", type=click.Choice(["spring_boot"]), help="The framework that should be used")
def main(dir, base_url, framework):
    """
    Find endpoints in source code of web applications.
    """
    writer = csv.DictWriter(sys.stdout, ["type", "url", "parameters", "file"])
    writer.writeheader()
    for endpoint in find_endpoints(dir, framework):
        writer.writerow({
            "type": endpoint.request_type,
            "url": Url(base_url) / endpoint.path,
            "file": endpoint.file,
            "parameters": ";".join((str(x) for x in endpoint.parameters))
        })


if __name__ == "__main__":
    main()
