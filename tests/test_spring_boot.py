import pytest
from endpoint_crawler import get_crawler
from pathlib import Path

dir = Path(__file__).parent

@pytest.fixture
def crawler():
    return get_crawler("spring_boot")

@pytest.fixture
def endpoints(crawler):
    return list(crawler.find_endpoints_file(dir / "resources/controller.java"))


def test_no_duplicates(crawler, endpoints):
    assert len(endpoints) == 2
    unique_paths = set((e.path for e in endpoints))
    assert len(unique_paths) == len(endpoints)


def test_correct_urls(crawler, endpoints):
    endpoints = list(crawler.find_endpoints_file(dir / "resources/controller.java"))
    assert len(endpoints) == 2
    paths = [e.path for e in endpoints]
    assert "rest/endpoint/request" in paths
    assert "rest/endpoint/check" in paths
