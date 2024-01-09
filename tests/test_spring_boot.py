import pytest
from endpoint_crawler import get_crawler
from pathlib import Path

dir = Path(__file__).parent
num_endpoints = 4

@pytest.fixture
def crawler():
    return get_crawler("spring_boot")

@pytest.fixture
def endpoints(crawler):
    return list(crawler.find_endpoints_file(dir / "resources/Controller.java"))


def test_no_duplicates(endpoints):
    assert len(endpoints) == num_endpoints
    unique_paths = set((e.path for e in endpoints))
    assert len(unique_paths) == len(endpoints)


def test_correct_urls(endpoints):
    assert len(endpoints) == num_endpoints
    paths = [e.path for e in endpoints]
    assert "rest/endpoint/request" in paths
    assert "rest/endpoint/check" in paths
    assert "rest/endpoint/data" in paths
    assert r"rest/endpoint/create/{id:[0-9-]+}" in paths

