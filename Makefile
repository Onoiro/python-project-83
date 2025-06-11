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


# Docker команды
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-restart:
	docker-compose restart

# Команды для разработки
dev-up:
	docker-compose -f docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Команды для продакшена
prod-deploy:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

# Утилиты
docker-clean:
	docker system prune -f
	docker volume prune -f

db-shell:
	docker-compose exec db psql -U abo -d pp83

app-shell:
	docker-compose exec app bash

# Резервное копирование БД
db-backup:
	docker-compose exec db pg_dump -U abo pp83 > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Восстановление БД
db-restore:
	docker-compose exec -T db psql -U abo pp83 < $(BACKUP_FILE)
