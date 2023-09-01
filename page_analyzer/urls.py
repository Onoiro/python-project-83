from urllib.parse import urlparse
import validators
from datetime import date
from .db import get_url_by_name, add_url


MAX_URL_LEN = 255


def get_correct_url(url):
    status = False
    category = 'danger'
    if len(url) > MAX_URL_LEN:
        message = 'URL превышает 255 символов'
        return status, message, category
    if not validators.url(url):
        message = 'Некорректный URL'
        return status, message, category
    url = normalize_url(url)
    url_data = get_url_data(url)
    if url_data:
        url_id = url_data['id']
        message = 'Страница уже существует'
        category = 'info'
    else:
        message = 'Страница успешно добавлена'
        category = 'success'
        created_at = date.today()
        url_data = add_url(url, created_at)
        url_id = url_data['id']
    return url_id, message, category


def normalize_url(url):
    url_parts = urlparse(url)
    url = f"{url_parts.scheme}://{url_parts.netloc}"
    return url


def get_url_data(url):
    url_data = get_url_by_name(url)
    return url_data
