import requests
from bs4 import BeautifulSoup
import re


def try_get_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as error:
        print(error)


def get_status_code(response):
    status_code = response.status_code
    return status_code


def get_url_seo_data(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1.string if soup.h1 else ''
    title = soup.title.string if soup.title else ''
    description = str(soup.find(attrs={"name": "description"}))
    pattern = r'"(.+?)"'
    description = re.search(pattern, description)
    description = description.group(1) if description else ''
    return h1, title, description
