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

@pytest.fixture
def paths(endpoints):
    return [e.path for e in endpoints]

def test_no_duplicates(endpoints):
    assert len(endpoints) == num_endpoints
    unique_paths = set((e.path for e in endpoints))
    assert len(unique_paths) == len(endpoints)


def test_correct_urls(paths):
    assert "rest/endpoint/request" in paths
    assert "rest/endpoint/check" in paths
    assert "rest/endpoint/data" in paths
    assert r"rest/endpoint/create/{id:[0-9-]+}" in paths


def test_parameters(endpoints):
    for e in endpoints:
        if e.path == r"rest/endpoint/create/{id:[0-9-]+}":
            assert len(e.parameters) == 2
            assert str(e.parameters[0]) == "@PathVariable long id"
            assert str(e.parameters[1]) == "@RequestBody MyClass value"
            for p in e.parameters:
                assert "@Something" not in str(p)
                assert "unimportant" not in str(p)
