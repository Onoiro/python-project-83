import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=DictCursor)
    except psycopg2.OperationalError:
        print('Can`t establish connection to database')
    return conn, cur


def close_db(conn, cur):
    conn.close()
    cur.close()


def get_all_urls():
    conn, cur = connect_db()
    cur.execute("SELECT * FROM urls ORDER BY id DESC")
    urls = cur.fetchall()
    close_db(conn, cur)
    return urls


def get_url_data(id):
    conn, cur = connect_db()
    cur.execute("SELECT * FROM urls WHERE id = (%s)", (id, ))
    url_data = cur.fetchone()
    close_db(conn, cur)
    return url_data


def get_url_checks(url_id):
    conn, cur = connect_db()
    cur.execute("SELECT * FROM url_checks WHERE url_id = (%s) \
                ORDER BY id DESC", (url_id, ))
    checks = cur.fetchall()
    close_db(conn, cur)
    return checks


def get_url_by_name(url):
    conn, cur = connect_db()
    cur.execute("SELECT * FROM urls WHERE name = (%s)", (url, ))
    url_data = cur.fetchone()
    close_db(conn, cur)
    return url_data


def add_url(url, created_at):
    conn, cur = connect_db()
    cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) \
                     RETURNING id', (url, created_at))
    conn.commit()
    url_data = cur.fetchone()
    close_db(conn, cur)
    return url_data


def add_url_check(id, status_code, h1, title,
                  description, check_created_at):
    conn, cur = connect_db()
    url_data = get_url_data(id)
    url_id = url_data['id']
    cur.execute("INSERT INTO url_checks \
                (url_id, status_code, h1, title, \
                description, created_at) \
                VALUES (%s, %s, %s, %s, %s, %s) \
                RETURNING id, status_code, created_at",
                (url_id, status_code, h1,
                 title, description, check_created_at))
    conn.commit()
    cur.execute("UPDATE urls \
                SET last_check = %s, status_code = %s WHERE id = %s",
                (check_created_at, status_code, id))
    conn.commit()
    close_db(conn, cur)
    return None
