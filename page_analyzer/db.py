import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db(func):
    def wrapper(*args, **kwargs):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor(cursor_factory=DictCursor)
        except psycopg2.OperationalError:
            print('Can`t establish connection to database')
            return None
        result = func(conn, cur, *args, **kwargs)
        conn.commit()
        close_db(conn, cur)
        return result
    return wrapper


def close_db(conn, cur):
    conn.close()
    cur.close()


@connect_db
def get_all_urls(conn, cur):
    cur.execute("SELECT * FROM urls ORDER BY id DESC")
    urls = cur.fetchall()
    return urls


@connect_db
def get_url_data(conn, cur, id):
    cur.execute("SELECT * FROM urls WHERE id = (%s)", (id, ))
    url_data = cur.fetchone()
    return url_data


@connect_db
def get_url_checks(conn, cur, url_id):
    cur.execute("SELECT * FROM url_checks WHERE url_id = (%s) \
                ORDER BY id DESC", (url_id, ))
    checks = cur.fetchall()
    return checks


@connect_db
def get_url_by_name(conn, cur, url):
    cur.execute("SELECT * FROM urls WHERE name = (%s)", (url, ))
    url_data = cur.fetchone()
    return url_data


@connect_db
def add_url(conn, cur, url, created_at):
    cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) \
                     RETURNING id', (url, created_at))
    url_data = cur.fetchone()
    return url_data


@connect_db
def add_url_check(conn, cur, id, status_code, h1, title,
                  description, check_created_at):
    url_data = get_url_data(id)
    url_id = url_data['id']
    cur.execute("INSERT INTO url_checks \
                (url_id, status_code, h1, title, \
                description, created_at) \
                VALUES (%s, %s, %s, %s, %s, %s) \
                RETURNING id, status_code, created_at",
                (url_id, status_code, h1,
                 title, description, check_created_at))
    cur.execute("UPDATE urls \
                SET last_check = %s, status_code = %s WHERE id = %s",
                (check_created_at, status_code, id))
    return None
