FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    curl \
    # nano \
    # procps \
    # net-tools \
    # iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

# Configure Poetry (disable virtual environment creation)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install

COPY page_analyzer/ ./page_analyzer/
COPY database.sql ./

# Create an unprivileged user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:8000", "page_analyzer.app:app"]
