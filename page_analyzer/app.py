#!/usr/bin/env python3

from flask import Flask, request, render_template, \
    redirect, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
import os
from .db import get_url_data, get_all_urls, get_url_checks, \
    get_url_by_name, add_url
from .urls import validate_url, check_url_len, normalize_url
from .parser import get_url_seo_data
from datetime import date


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
    if check_url_len(input):
        flash('URL превышает 255 символов', 'danger')
        return render_template('index.html'), 422
    if validate_url(input):
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422
    url = normalize_url(input)
    url_data = get_url_by_name(url)
    if url_data:
        flash('Страница уже существует', 'info')
    else:
        created_at = date.today()
        url_data = add_url(url, created_at)
        flash('Страница успешно добавлена', 'success')
    url_id = url_data['id']
    return redirect(url_for('url', url_id=url_id))


@app.post('/urls/<id>/checks')
def checks(id):
    message, category = get_url_seo_data(id)
    flash(message, category)
    return redirect(url_for('url', url_id=id))


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
