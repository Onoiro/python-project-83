install:
	poetry install

build:
	./build.sh

publish:
	poetry publish --dry-run

dev:
	poetry run flask --app page_analyzer/app --debug run

# Загрузка значения переменной PORT из .env файла или 8000 по умолчанию
# PORT ?= $(shell sed -n 's/^PORT=\(.*\)/\1/p' .env || echo 8000)
PORT ?= 8000
check:
	@echo "PORT is set to: $(PORT)"

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

lint:
	poetry run flake8 page_analyzer/

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl
