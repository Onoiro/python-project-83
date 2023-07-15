#!/usr/bin/env python3

from flask import Flask, request, render_template, \
                  redirect, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
import os
from datetime import date
from urllib.parse import urlparse
import validators
import requests


app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
print(DATABASE_URL)


def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=DictCursor)
    except psycopg2.OperationalError:
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
    cur.execute("SELECT * FROM url_checks WHERE url_id = (%s)", (url_id, ))
    checks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template(
        'url.html',
        messages=messages,
        id=url_id,
        name=url_data['name'],
        created_at=url_data['created_at'],
        checks=checks
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
    created_at = date.today()
    conn, cur = connect_db()
    cur.execute("SELECT * FROM urls WHERE name = (%s)", (url, ))
    # if url not exist url_data will get None so need except TypeError
    url_data = cur.fetchone()
    try:
        url_id = url_data['id']
        flash('Страница уже существует', 'info')
    except TypeError:  # if URL not exist
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) \
                     RETURNING id', (url, created_at))
        conn.commit()
        url_data = cur.fetchone()
        url_id = url_data['id']
        flash('Страница успешно добавлена', 'success')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('url', url_id=url_id))


@app.post('/urls/<id>/checks')
def checks(id):
    conn, cur = connect_db()
    cur.execute("SELECT * FROM urls WHERE id = (%s)", (id, ))
    url_data = cur.fetchone()
    url_id = url_data['id']
    r = requests.get(url_data['name'])
    print(r.status_code)
    status_code = r.status_code
    check_created_at = date.today()
    flash('Страница успешно проверена', 'success')
    cur.execute('INSERT INTO url_checks (url_id, status_code, created_at) VALUES (%s, %s, %s) \
                     RETURNING id', (url_id, status_code, check_created_at))
    conn.commit()
    check_url_data = cur.fetchone()
    check_id = check_url_data['id']
    cur.execute('UPDATE urls SET last_check = %s \
                WHERE id = "id"', (check_created_at, ))
    conn.commit()
    return redirect(url_for(
        'url',
        check_id=check_id,
        url_id=url_id,
        status_code=status_code,
        check_created_at=check_created_at
        ))


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404
