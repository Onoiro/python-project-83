# Используем Python 3.8 как базовый образ
FROM python:3.8-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы конфигурации Poetry
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install poetry

# Настраиваем Poetry (отключаем создание виртуального окружения)
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install

# Копируем исходный код приложения
COPY page_analyzer/ ./page_analyzer/
COPY database.sql ./

# Создаем непривилегированного пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Экспонируем порт 8000
EXPOSE 8000

# Команда запуска по умолчанию
CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:8000", "page_analyzer.app:app"]
