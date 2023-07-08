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
    return render_template('index.html')


@app.get('/urls/')
def urls():
    conn, cur = connect_db()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("SELECT * FROM urls")
        urls = reversed(cur.fetchall())
    return render_template(
        'urls.html',
        urls=urls
    )


@app.get('/urls/<url_id>')
def url(url_id):
    messages = get_flashed_messages(with_categories=True)
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
    input = request.form.get('url')
    if len(input) > 255:
        flash('URL превышает 255 символов', 'danger')
        return redirect(url_for('index'))
    if not validators.url(input):
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))
    url_parts = urlparse(input)
    url = f"{url_parts.scheme}://{url_parts.netloc}"
    created_at = datetime.now()
    conn, cur = connect_db()
    try:
        cur.execute("SELECT * FROM urls WHERE name = (%s)", (url, ))
        url_data = cur.fetchone()
        url_id = url_data['id']
        flash('Страница уже существует', 'info')
    except:
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (url, created_at))
        conn.commit()
        url_data = cur.fetchone()
        url_id = url_data['id']
        flash('Страница успешно добавлена', 'success')
    cur.close()
    conn.close()
    return redirect(url_for('url', url_id=url_id))


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
