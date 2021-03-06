
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  test        Runs tests"
	@echo "  test-all    Runs tests using tox"
	@echo "  release     Makes a release"

test:
	@pytest tests

coverage:
	@pytest\
		--verbose\
		--cov graphql_geojson\
		--cov-config .coveragerc\
		--cov-report term\
		--cov-report xml

test-all:
	@tox

release:
	@python setup.py sdist upload
	@python setup.py bdist_wheel upload

.PHONY: help test coverage test-all release
