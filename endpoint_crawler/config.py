import os
from dynaconf import Dynaconf
from pathlib import Path

dir = Path(__file__).parent

settings = Dynaconf(
    envvar_prefix="ENDPOINT_CRAWLER",
    settings_files=[
        dir / '../settings.toml',
        Path(os.environ['HOME']) / '.config' / 'endpoint_crawler' / 'settings.toml'
    ],
)
