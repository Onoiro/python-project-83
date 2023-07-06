#!/usr/bin/env python3

from flask import Flask, request, make_response, render_template, \
                  redirect, url_for, flash, get_flashed_messages, session
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
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
        cur = conn.cursor(cursor_factory=DictCursor)
    except:
        print('Can`t establish connection to database')
    return conn, cur


@app.get('/')
def index():
    term = request.args.get('url', '', type=str)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )


@app.get('/urls/')
def urls():
    return render_template(
        'urls.html'
    )


@app.get('/urls/<url_id>')
def url(url_id):
    messages = get_flashed_messages(with_categories=True)
    # url_data = {}
    conn, cur = connect_db()
    cur.execute("SELECT * FROM urls WHERE id = (%s)", (url_id, ))
    url_data = cur.fetchone()
    cur.close()
    conn.close()
    return render_template(
        'url.html',
        messages=messages,
        id=url_id,
        name=url_data['name'],
        created_at=url_data['created_at']
    )


@app.post('/urls/')
def urls_post():
    if not validators.url(request.form.get('url')):
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))
    url_parts = urlparse(request.form.get('url'))
    url = f"{url_parts.scheme}://{url_parts.netloc}"
    created_at = datetime.now()
    conn, cur = connect_db()
    try:
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (url, created_at))
        url_data = cur.fetchone()
        url_id = url_data['id']
        print(url_id)
        conn.commit()
        cur.close()
        conn.close()
        flash('Страница успешно добавлена', 'success')
    except psycopg2.errors.UniqueViolation:
        flash('Страница уже существует', 'info')
    return redirect(url_for('url', url_id=url_id))
    # return redirect(url_for('index', url_id=url_id))


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
