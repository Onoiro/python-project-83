#!/usr/bin/env python3

from flask import Flask, request, render_template, \
    redirect, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
import os
from .db import get_url_data, get_all_urls, get_url_checks
from .urls import get_correct_url, get_url_seo_data


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
        return render_template('index.html'), 422
    flash(message, category)
    return redirect(url_for('url', url_id=url))


@app.post('/urls/<id>/checks')
def checks(id):
    message, category = get_url_seo_data(id)
    flash(message, category)
    return redirect(url_for('url', url_id=id))


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
