.PHONY: tests install run

run:
	python -m endpoint_crawler --help

install:
	pip install -e .

tests:
	python -m pytest tests --cov=./endpoint_crawler -s
