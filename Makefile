install:
	poetry install

build:
	./build.sh

publish:
	poetry publish --dry-run

dev:
	poetry run flask --app page_analyzer/app --debug run

PORT ?= 8000
check:
	@echo "PORT is set to: $(PORT)"

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

lint:
	poetry run flake8 page_analyzer/

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-restart:
	docker compose restart

prod-deploy:
	docker compose down
	docker compose build --no-cache --pull
	docker compose up -d

docker-clean:
	docker system prune -f
	docker volume prune -f

app-shell:
	docker compose exec app bash

POSTGRES_USER := $(shell docker compose exec db printenv POSTGRES_USER)
POSTGRES_DB := $(shell docker compose exec db printenv POSTGRES_DB)
db-shell:
	docker compose exec db psql \
		-U $(POSTGRES_USER) \
		-d $(POSTGRES_DB)

db-backup:
	docker compose exec db pg_dump \
		-U $(POSTGRES_USER) $(POSTGRES_DB) \
		> backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore:
	docker compose exec -T db psql \
		-U $(POSTGRES_USER) \
		-d $(POSTGRES_DB) \
		< $(BACKUP_FILE)
