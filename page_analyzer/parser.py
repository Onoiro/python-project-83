import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from .db import add_url_check


def get_url_seo_data(url, id):
    try:
        r = requests.get(url)
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
        add_url_check(id, status_code, h1, title,
                      description, check_created_at)
    except requests.exceptions.RequestException:
        message = 'Произошла ошибка при проверке'
        category = 'danger'
    return message, category
