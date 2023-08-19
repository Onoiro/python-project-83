from urllib.parse import urlparse
import validators
# import requests
# from bs4 import BeautifulSoup
# import re
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
    url_parts = urlparse(url)
    url = f"{url_parts.scheme}://{url_parts.netloc}"
    url_data = get_url_by_name(url)
    # if url not exist url_data will get None so need except TypeError
    try:
        url_id = url_data['id']
        message = 'Страница уже существует'
        category = 'info'
    # if URL not exist
    except TypeError:
        message = 'Страница успешно добавлена'
        category = 'success'
        created_at = date.today()
        url_data = add_url(url, created_at)
        url_id = url_data['id']
    return url_id, message, category
