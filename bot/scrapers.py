import json
import re

import lxml.html
import requests

import models
from bot.message import generate


def xkom() -> models.Promotion:
    return _xkom_alto('https://x-kom.pl', 'xkom')


def alto() -> models.Promotion:
    return _xkom_alto('https://al.to', 'alto')


def _xkom_alto(base_url: str, shop: str) -> models.Promotion:
    response = requests.get(base_url)
    tree = lxml.html.fromstring(response.text)
    hot_shot = tree.xpath('//div[@id="hotShot"]')[0]

    old_price = hot_shot.xpath('.//div[@class="old-price"]')[0].text
    old_price = _price_parser(old_price)
    new_price = hot_shot.xpath('.//div[@class="new-price"]')[0].text
    new_price = _price_parser(new_price)
    product_name = hot_shot.xpath('.//p[@class="product-name"]')[0].text

    hot_shot_script = hot_shot.xpath('following-sibling::script')[0].text
    match = re.search(r'window\.location ?= ?(?P<link>.*);', hot_shot_script)
    url = base_url + json.loads(match.group('link'))
    return models.Promotion(
        shop=shop,
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=url,
    )


def _price_parser(price: str) -> float:
    match = re.search(r'(?P<zlotowki>\d+)(,(?P<grosze>\d+))?', price)
    zlotowki = int(match.group('zlotowki'))
    grosze = match.group('grosze')
    grosze = int(grosze) if grosze else 0
    return zlotowki + grosze / 100


def morele() -> models.Promotion or None:
    response = requests.get('https://www.morele.net/')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[@class="promotion-product"]')
    if not promo:
        return
    else:
        promo = promo[0]
    product_link = promo.xpath('.//div[@class="product-name"]/a')[0]
    product_name = product_link.text.strip()
    product_url = product_link.get('href')
    price = promo.xpath('.//div[@class="product-price"]')[0]
    old_price = price.xpath('.//div[contains(@class, "old")]/span')[0].text.strip()
    old_price = _price_parser(old_price)
    new_price = price.xpath('.//div[contains(@class, "new")]/span')[0].text.strip()
    new_price = _price_parser(new_price)
    code = promo.xpath('.//div[@class="product-code"]')[0].text.strip()
    match = re.search(r'użyj kodu:? (.*)', code)
    code = match.group(1)
    return models.Promotion(
        shop='morele',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        code=code,
    )


if __name__ == '__main__':
    print(generate(morele()))
