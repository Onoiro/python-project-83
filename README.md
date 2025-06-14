[![Actions Status](https://github.com/Onoiro/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Onoiro/weban/actions)
![WebAnalyzer Actions](https://github.com/Onoiro/weban/actions/workflows/page-analyzer-check.yml/badge.svg)
[![Maintainability](https://qlty.sh/badges/d5121bbd-7936-477b-84a2-79036a786623/maintainability.svg)](https://qlty.sh/gh/Onoiro/projects/weban)

## Welcome to [WebAnalyzer](https://weban.2-way.ru)
Use this application for minimal SEO analysis of websites.

Visit [https://weban.2-way.ru](https://weban.2-way.ru) to try WebAnalyzer

Check website accessibility and presence of \<h1\>, \<title\> tags, and \<meta\> tag with attribute name="description" content="...".

## Requirements

#### For local installation without Docker:
* OS Linux/macOS
* Python >= 3.8.1
* Poetry >= 1.2.2
* PostgreSQL >= 12.15

#### For Docker deployment:
* Docker Engine >= 20.10
* Docker Compose >= 2.0

## Installation and Setup

#### Option 1: Run with Docker (Recommended)
```bash
# clone the repository
git clone https://github.com/Onoiro/weban.git
cd weban

# create environment variables file
touch .env

# open .env file for edit
nano .env

# add the following variables (edit values as needed):
POSTGRES_DB=webanalyzer_db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key_here

# build and start all services
make docker-up

# or use Docker Compose directly:
docker compose up -d

# view logs
make docker-logs

# or:
docker compose logs -f
```
The application will be available at: http://localhost:8000

**Additional Docker commands:**
```bash
# Stop the application
make docker-down

# Restart services
make docker-restart

# Connect to application container
make app-shell

# Connect to database
make db-shell

# Create database backup
make db-backup

# Restore database from backup
make db-restore BACKUP_FILE=backup_20231201_120000.sql

# Production deployment (with rebuild)
make prod-deploy

# Clean up Docker resources
make docker-clean
```

#### Option 2: Local Installation without Docker
```bash
# clone the repository
git clone https://github.com/Onoiro/weban.git
cd weban

# create PostgreSQL database (replace parameters with your own)
sudo -u postgres createdb --owner=your_user webanalyzer_db

# Create .env file and configure environment variables
touch .env

# open .env file for edit
nano .env

# add environment variables:
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/webanalyzer_db
SECRET_KEY=your_secret_key_here

# install dependencies and initialize DB
make build

# or run commands separately:
make install
psql -a -d $DATABASE_URL -f database.sql

# start the application in development mode
make dev

# start the application in production mode
make start

# or specify custom port:
PORT=8080 make start
```
**Additional development commands:**

```bash
# code linting
make lint

# install package locally
make package-install
```

## Usage

After starting the application, open your browser and navigate to:

    When using Docker: http://localhost:8000
    For local setup: http://localhost:5000 (development mode) or http://localhost:8000 (production)

Enter a website URL for analysis and get a report on its SEO suitability.


## Project Architecture
* Backend: Flask (Python)
* Database: PostgreSQL
* Deployment: Docker + Docker Compose
* Web Server: Gunicorn
* Dependency Management: Poetry


## Troubleshooting

### Docker Issues:

**Port already in use:**
```bash
# Check which process is using port 8000
sudo netstat -tlnp | grep :8000

# or
sudo lsof -i:8000

# Change port in docker-compose.yml or stop conflicting service
```
**Permission issues:**
```bash
# Make sure Docker is running and you have permissions
sudo systemctl start docker
sudo usermod -aG docker $USER
# Re-login after adding to group
```
**Database not ready:**
```bash
# Check service health status
docker compose ps
```

### Local Installation Issues:

**Database connection errors:**
* Verify DATABASE_URL is correct
* Make sure PostgreSQL is running
* Check user permissions for the database

### Poetry issues:

```bash
# Update Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Clear cache
poetry cache clear pypi --all
```

### License
This project is educational and created as part of Hexlet learning program.
