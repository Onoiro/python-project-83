[![Actions Status](https://github.com/Onoiro/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Onoiro/python-project-83/actions)
![Page Analyzer Actions](https://github.com/Onoiro/python-project-83/actions/workflows/page-analyzer-check.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/3807cda22bbcca6fee03/maintainability)](https://codeclimate.com/github/Onoiro/python-project-83/maintainability)

## Welcome to [Page-analyzer](https://page-analyzer-tdcb.onrender.com/)
Use this application for a minimal SEO analysis of a website.

Click [https://page-analyzer-tdcb.onrender.com/](https://page-analyzer-tdcb.onrender.com/) to get Page-analyzer

Check website accessibility and presence of \<h1\>, \<title\> tags, and \<meta\> tag with attribute name="description" content="...".

## Install for personal local use
```bash
git clone https://git@github.com:Onoiro/python-project-83.git
cd python-project-83

# build app & connect to database:
# poetry install && psql -a -d $DATABASE_URL -f database.sql
make build

# create .env file contains environment variables
touch .env
nano .env

# specify environment variables in .env, for example:
DATABASE_URL=postgresql://user:password@connect_url/database
SECRET_KEY="secret_key"

# run in development mode:
# poetry run flask --app page_analyzer/app --debug run
make dev

# run production:
# (PORT ?= 8000)
# poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app
make start
```
### Requirements
* OS Linux  
* python = ^3.8.1
* poetry = ^1.2.2
* postgres = ^12.15
