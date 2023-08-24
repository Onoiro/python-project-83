from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from .db import get_url_data, get_url_by_name, add_url, add_url_check


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


def get_url_seo_data(id):
    url_data = get_url_data(id)
    # url_id = url_data['id']
    try:
        r = requests.get(url_data['name'])
        r.raise_for_status()
        status_code = r.status_code
        check_created_at = date.today()
        soup = BeautifulSoup(r.text, 'html.parser')
        h1 = soup.h1
        h1 = soup.h1.string if h1 else ''
        title = soup.title
        title = soup.title.string if title else ''
        description = str(soup.find(attrs={"name": "description"}))
        pattern = r'"(.+?)"'
        description = re.search(pattern, description)
        description = description.group(1) if description else ''
        message = 'Страница успешно проверена'
        category = 'success'
        # flash('Страница успешно проверена', 'success')
        add_url_check(id, status_code, h1, title,
                      description, check_created_at)
    except requests.exceptions.RequestException:
        message = 'Произошла ошибка при проверке'
        category = 'danger'
        # flash('Произошла ошибка при проверке', 'danger')
    return message, category
