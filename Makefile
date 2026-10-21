.PHONY: install test-baseline test-evaluation test-all docker-fixed

install:
	python -m pip install -e '.[test]'

test-baseline:
	pytest -q tests

test-evaluation:
	pytest -q evaluation

test-all:
	pytest -q tests evaluation

docker-fixed:
	docker compose run --build --rm fixed-tests
