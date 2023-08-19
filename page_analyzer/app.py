#!/usr/bin/env python3

from flask import Flask, request, render_template, \
    redirect, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
import os
from datetime import date
from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup
import re
from .db import get_url_data, get_all_urls, \
    get_url_checks, get_url_by_name, add_url, add_url_check
from .urls import get_correct_url


app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls/')
def urls():
    urls = reversed(get_all_urls())
    return render_template(
        'urls.html',
        urls=urls
    )


@app.get('/urls/<url_id>')
def url(url_id):
    messages = get_flashed_messages(with_categories=True)
    url_data = get_url_data(url_id)
    name = url_data['name']
    created_at = url_data['created_at']
    checks = reversed(get_url_checks(url_id))
    return render_template(
        'url.html',
        messages=messages,
        id=url_id,
        name=name,
        created_at=created_at,
        checks=checks
    )


@app.post('/urls')
def urls_post():
    input = request.form.get('url')
    url, message, category = get_correct_url(input)
    if url is False:
        flash(message, category)
        return redirect(url_for('index'))
    # url_data = get_url_by_name(url)
    # try:
    #     url_id = url_data['id']
    #     flash('Страница уже существует', 'info')
    # # if URL not exist
    # except TypeError:
    #     created_at = date.today()
    #     url_data = add_url(url, created_at)
    #     url_id = url_data['id']
    #     flash('Страница успешно добавлена', 'success')
    # url_id, message, category = get_url_id(url)
    flash(message, category)
    return redirect(url_for('url', url_id=url))


@app.post('/urls/<id>/checks')
def checks(id):
    url_data = get_url_data(id)
    url_id = url_data['id']
    try:
        r = requests.get(url_data['name'])
        r.raise_for_status()
        status_code = r.status_code
        check_created_at = date.today()
        soup = BeautifulSoup(r.text, 'html.parser')
        h1 = soup.h1
        h1 = soup.h1.string if h1 else ''
        title = soup.title
        title = soup.title.string if title else ''
        description = str(soup.find(attrs={"name": "description"}))
        pattern = r'"(.+?)"'
        description = re.search(pattern, description)
        description = description.group(1) if description else ''
        flash('Страница успешно проверена', 'success')
        add_url_check(id, status_code, h1, title,
                      description, check_created_at)
        return redirect(url_for(
            'url',
            check_id=id,
            url_id=url_id,
            h1=h1,
            status_code=status_code,
            title=title,
            check_created_at=check_created_at
        ))
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url', url_id=url_id), 302)


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
