install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

start:
	poetry run flask --app page_analyzer/app --debug run

dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer/app.py

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=app --cov-report xml

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl
