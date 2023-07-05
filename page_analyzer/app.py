#!/usr/bin/env python3

from flask import Flask, request, make_response, render_template, \
                  redirect, url_for, flash, get_flashed_messages, session
from dotenv import load_dotenv
import psycopg2
import os
from datetime import datetime
from urllib.parse import urlparse
import validators


app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
print(DATABASE_URL)


def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
    except:
        print('Can`t establish connection to database')
    return conn, cur


@app.get('/')
def index():
    term = request.args.get('url', '', type=str)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        h1 = "Анализатор страниц",
        messages=messages,
        search=term
    )


@app.post('/urls/')
def urls_post():
    if not validators.url(request.form.get('url')):
        flash('Некорректный URL','danger')
        return redirect(url_for('index'))
    url_parts = urlparse(request.form.get('url'))
    url = f"{url_parts.scheme}://{url_parts.netloc}"
    created_at = datetime.now()
    conn, cur = connect_db()
    try:
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (url, created_at))
        conn.commit()
        cur.close()
        conn.close()
        flash('Страница успешно добавлена', 'success')
    except psycopg2.errors.UniqueViolation:
        flash('Страница уже существует', 'info')
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
