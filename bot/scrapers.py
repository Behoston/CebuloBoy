import datetime
import json
import random
import re

import lxml.html
import requests

import models


def xkom() -> models.Promotion:
    return _xkom_alto(
        base_url='https://x-kom.pl',
        shop='xkom',
        promo_end_morning=10,
        promo_end_evening=22,
    )


def alto() -> models.Promotion:
    return _xkom_alto(
        base_url='https://al.to',
        shop='alto',
        promo_end_morning=9,
        promo_end_evening=21,
    )


def _xkom_alto(base_url: str, shop: str, promo_end_morning: int, promo_end_evening: int) -> models.Promotion:
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
    end_date = datetime.datetime.now()
    if end_date.hour < 12:
        end_date = end_date.replace(hour=promo_end_evening, minute=0, second=0)
    else:
        end_date = end_date.replace(hour=promo_end_morning, minute=0, second=0) + datetime.timedelta(days=1)
    try:
        left, sold = [int(i.text) for i in hot_shot.xpath('.//*[contains(@class,"count")]//strong')]
    except Exception as e:
        print(e)
        left, sold = None, None
    return models.Promotion(
        shop=shop,
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=url,
        end_date=end_date,
        items_available=left,
        items_sold=sold,
    )


def _price_parser(price: str) -> float:
    match = re.search(r'(?P<zlotowki>[\d\s]+)([,.]\s*(?P<grosze>\d+))?', price)
    zlotowki = re.sub(r'\s', '', match.group('zlotowki'))
    zlotowki = int(zlotowki)
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
    if match:
        code = match.group(1)
    else:
        code = None
    end_date = promo.xpath('.//div[@class="morele-countdown promotion-countdown"]')[0].get('data-date-to')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    count = promo.xpath('.//div[@class="product-availability-info"]')[0]
    sold = int(count.xpath('.//div[@class="orders"]//div[contains(@class, "number")]')[0].text)
    left = int(count.xpath('.//div[@class="quantity"]//div[contains(@class, "number")]')[0].text)
    return models.Promotion(
        shop='morele',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        code=code,
        end_date=end_date,
        items_available=left,
        items_sold=sold,
    )


def hard_pc() -> models.Promotion or None:
    response = requests.get('https://sklep.hard-pc.pl/')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[contains(@class, "hot-deal")]//div[@class="item-info"]')
    if not promo:
        return
    else:
        promo = promo[0]
    product_link = promo.xpath('.//a')[0]
    product_name = product_link.text.strip()
    product_url = 'https://sklep.hard-pc.pl/' + product_link.get('href').split('?')[0]
    price = promo.xpath('.//span[@class="price"]')[0]
    old_price = price.xpath('.//strike')[0].text.strip()
    old_price = _price_parser(old_price)
    new_price = price.xpath('.//span')[0].text.strip()
    new_price = _price_parser(new_price)
    end_date = tree.xpath('//script[not(@src)]')[1].text
    for line in end_date.split('\n'):
        if line.strip().startswith('date'):
            end_date = line.strip().split(': ')[-1].strip(',').strip('"')
    end_date = datetime.datetime.strptime(end_date, '%d %B %Y %H:%M:%S')
    return models.Promotion(
        shop='hard-pc',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        end_date=end_date,
    )


def komputronik() -> [models.Promotion]:
    response = requests.get('https://www.komputronik.pl/frontend-api/product/box/occasions')
    promotions = response.json()
    return [
        models.Promotion(
            shop='komputronik',
            product_name=promotion['name'],
            old_price=_price_parser(promotion['prices']['price_base_gross']),
            new_price=_price_parser(promotion['prices']['price_gross']),
            url=promotion['url'],
            end_date=datetime.datetime.strptime(promotion['date_to_end_promotion'], '%Y/%m/%d %H:%M:%S'),
            items_available=promotion['available_quantity'],
            items_sold=promotion['ordered_quantity'],
        ) for promotion in promotions['products']
    ]


def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        (
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/67.0.3396.99 Safari/537.36'
        ),
        (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'
        ),
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        (
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.51'
        ),
    ]
    return random.choice(user_agents)


def proline() -> models.Promotion or None:
    session = requests.session()
    session.headers['User-Agent'] = get_random_user_agent()
    response = session.get('https://proline.pl/')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[@id="headshot"]')
    if not promo:
        return
    else:
        promo = promo[0]
    try:
        product_link = promo.xpath('.//h2/a')[0]
    except IndexError:
        return None
    product_name = product_link.text.strip()
    product_url = 'https://proline.pl' + product_link.get('href').split('?')[0]
    old_price = promo.xpath('.//*[@class="cena_old"]/b')[0].text.strip()
    old_price = _price_parser(old_price)
    new_price = promo.xpath('.//*[@class="cena_new"]/b')[0].text.strip()
    new_price = _price_parser(new_price)
    end_date = promo.xpath('./script')[0].text
    year, month, day, hour, minute = re.findall('\d+', end_date)
    end_date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
    response = session.get('https://proline.pl/headshot-ilosc.php')
    tree = lxml.html.fromstring(response.text)
    left, sold = [int(i.text) for i in tree.xpath('//b')]
    return models.Promotion(
        shop='proline',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        end_date=end_date,
        items_available=left,
        items_sold=sold,
    )


def wlodipol() -> models.Promotion or None:
    response = requests.get('https://wlodipol.pl')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[contains(@class, "hotdeal-box")]//div[@class="product-info"]')
    if not promo:
        return
    else:
        promo = promo[0]
    product_link = promo.xpath('.//a[@class="product-name"]')[0]
    product_name = product_link.text.strip()
    product_url = product_link.get('href')
    old_price = promo.xpath('.//span[contains(@class, "price old")]')[0].text
    new_price = promo.xpath('.//span[contains(@class, "price new")]')[0].text
    old_price = _price_parser(old_price)
    new_price = _price_parser(new_price)
    end_date = promo.xpath('//div[@class="countdown"]')[0].text.strip()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    return models.Promotion(
        shop='wlodipol',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        end_date=end_date,
    )


if __name__ == '__main__':
    from bot.message import generate

    print(generate(proline()))
