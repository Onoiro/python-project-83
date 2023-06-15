install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

dev:
	poetry run flask --app page_analyzer/app --debug run

# PORT ?= 8000
# start:
# 	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

start:
	poetry run gunicorn --workers=5 --bind=127.0.0.1:8000 page_analyzer.app:app

lint:
	poetry run flake8 page_analyzer/app.py

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=app --cov-report xml

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl
