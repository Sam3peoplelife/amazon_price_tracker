import re
from bs4 import BeautifulSoup
import requests


def get_link_data(url):
    headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en",
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    name = soup.select_one(selector="#productTitle").getText().strip()
    price = soup.select_one(selector=".a-price-whole").getText()
    price = re.sub(r'\D', '', price)

    return name, price