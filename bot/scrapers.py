import datetime
import json
import random
import re
import typing

import lxml.html
import requests

import models


def xkom() -> typing.List[models.Promotion]:
    return _xkom_alto(
        base_url='https://www.x-kom.pl',
        shop='xkom',
    )


def alto() -> typing.List[models.Promotion]:
    return _xkom_alto(
        base_url='https://www.al.to',
        shop='alto',
    )


def combat() -> typing.List[models.Promotion]:
    response = requests.get(url='https://www.combat.pl/rest/V1/get-hot-shot')
    data = response.json()[0]

    return [models.Promotion(
        shop='combat',
        product_name=data['title'],
        old_price=float(data['regularPrice'].strip('\xa0zł</span>').strip('<span class="price">').replace(',', '.')),
        new_price=float(data['promoPrice'].strip('\xa0zł</span>').strip('<span class="price">').replace(',', '.')),
        url=f'https://www.combat.pl/goracy_strzal/{data["promotionId"]}',
        end_date=datetime.datetime.now() + datetime.timedelta(seconds=data['total']),
        items_available=data['left'],
        items_sold=data['sold'],
    )]


def _xkom_alto(base_url: str, shop: str) -> typing.List[models.Promotion]:
    session = requests.session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    response = session.get(base_url)
    tree = lxml.html.fromstring(response.text)
    script_data = tree.xpath('//script[not(@type) and contains(text(), "hotShot")]')[0].text
    match = re.search(r"window.__INITIAL_STATE__\['app']\s+=\s+(?P<data>.*);", script_data)
    data = json.loads(match.group('data'))
    hot_shot_data = data['productsLists']['hotShot'][0]['extend']
    old_price = hot_shot_data['oldPrice']
    new_price = hot_shot_data['price']
    product_name = hot_shot_data['promotionName']
    promo_id = hot_shot_data['id']
    url = f'{base_url}/goracy_strzal/{promo_id}'
    end_date = datetime.datetime.fromisoformat(hot_shot_data['promotionEnd'].replace('Z', '+00:00')).astimezone()
    sold = hot_shot_data['saleCount']
    left = hot_shot_data['promotionTotalCount'] - sold
    return [models.Promotion(
        shop=shop,
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=url,
        end_date=end_date,
        items_available=left,
        items_sold=sold,
    )]


def morele() -> typing.List[models.Promotion]:
    response = requests.get('https://www.morele.net/')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[@class="home-sections-promotion"]')
    if not promo:
        return []
    else:
        promo = promo[0]
    product_link = promo.xpath('.//div[@class="promo-box-name"]/a')[0]
    product_name = product_link.text.strip()
    product_url = product_link.get('href')
    price = promo.xpath('.//div[@class="promo-box-price"]')[0]
    old_price = price.xpath('.//div[contains(@class, "old")]')[1].tail.strip()
    old_price = price_parser(old_price)
    new_price = price.xpath('.//div[contains(@class, "new")]')[1].tail.strip()
    new_price = price_parser(new_price)
    code = promo.xpath('.//div[@class="promo-box-code"]/div[@class="promo-box-code-value"]')
    if code:
        code = code[0].text.strip()
    else:
        code = None
    end_date = promo.xpath('.//div[@class="promo-box-countdown"]')[0].get('data-date-to')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    sold = promo.xpath('.//div[@class="status-box-expired"]')[0].text
    sold = int(re.findall(r'\d+', sold)[0])
    left = promo.xpath('.//div[@class="status-box-was"]')[0].text
    left = int(re.findall(r'\d+', left)[0])
    return [models.Promotion(
        shop='morele',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        code=code,
        end_date=end_date,
        items_available=left,
        items_sold=sold,
    )]


def hard_pc() -> typing.List[models.Promotion]:
    response = requests.get('https://sklep.hard-pc.pl/')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//article[@class="box-f"]/div')
    if not promo:
        return []
    else:
        promo = promo[0]
    product_link = promo.xpath('.//h3/a')[0]
    product_name = product_link.text.strip()
    product_url = 'https://sklep.hard-pc.pl/' + product_link.get('href').split('?')[0].strip()
    price = promo.xpath('.//p[@class="prices"]')[0]
    old_price = price.xpath('.//span[@class="old"]')[0].text.strip()
    old_price = price_parser(old_price)
    new_price = price.xpath('.//span[@class="default promo"]')[0].text.strip()
    new_price = price_parser(new_price)
    return [models.Promotion(
        shop='hard-pc',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        end_date=None,
    )]


def komputronik() -> typing.List[models.Promotion]:
    session = requests.session()
    session.headers['User-Agent'] = get_random_user_agent()
    response = session.get('https://www.komputronik.pl/frontend-api/product/box/occasions')
    print(response)
    promotions = response.json()
    return [
        models.Promotion(
            shop='komputronik',
            product_name=promotion['name'],
            old_price=price_parser(promotion['prices']['price_base_gross']),
            new_price=price_parser(promotion['prices']['price_gross']),
            url=promotion['url'],
            end_date=datetime.datetime.strptime(promotion['date_to_end_promotion'], '%Y/%m/%d %H:%M:%S'),
            items_available=promotion['available_quantity'],
            items_sold=promotion['ordered_quantity'],
        ) for promotion in promotions['products']
    ]


def proline() -> typing.List[models.Promotion]:
    session = requests.session()
    session.headers['User-Agent'] = get_random_user_agent()
    response = session.get('https://proline.pl/')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[@id="headshot"]')
    if not promo:
        return []
    else:
        promo = promo[0]
    try:
        product_link = promo.xpath('.//h2/a')[0]
    except IndexError:
        return []
    product_name = product_link.text.strip()
    product_url = 'https://proline.pl' + product_link.get('href').split('?')[0]
    old_price = promo.xpath('.//*[@class="cena_old"]/b')[0].text.strip()
    old_price = price_parser(old_price)
    new_price = promo.xpath('.//*[@class="cena_new"]/b')[0].text.strip()
    new_price = price_parser(new_price)
    end_date = promo.xpath('./script')[0].text
    year, month, day, hour, minute = re.findall(r'\d+', end_date)
    end_date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
    response = session.get('https://proline.pl/headshot-ilosc.php')
    tree = lxml.html.fromstring(response.text)
    left, sold = [int(i.text) for i in tree.xpath('//b')]
    return [models.Promotion(
        shop='proline',
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        url=product_url,
        end_date=end_date,
        items_available=left,
        items_sold=sold,
    )]

def amso() -> typing.List[models.Promotion]:
    base_url = 'https://amso.pl/'
    response = requests.get(base_url)
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[@id="main_hotspot_zone1"]')[0]
    link = promo.xpath('.//a[@class="product-name"]')
    new_price = price_parser(promo.xpath('.//*[@class="price"]')[0].text)
    old_price = price_parser(promo.xpath('.//*[@class="max-price"]')[0].text)
    items_and_date = promo.xpath('.//*[contains(@class,"product_timer ")]')[0]
    end_date = datetime.date.fromisoformat(items_and_date.get('data-date'))
    end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
    total_item = int(items_and_date.get('data-init-amount'))
    available_item = int(items_and_date.get('data-amount'))
    return [models.Promotion(
        shop='amso',
        product_name=link[0].text,
        old_price=old_price,
        new_price=new_price,
        url=base_url + link[0].get('href'),
        end_date=end_datetime,
        items_available=available_item,
        items_sold=total_item - available_item,
    )]


def get_random_user_agent() -> str:
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


def price_parser(price: str) -> float:
    match = re.search(r'(?P<zlotowki>[\d\s]+)([,.]\s*(?P<grosze>\d+))?', price)
    zlotowki = re.sub(r'\s', '', match.group('zlotowki'))
    zlotowki = int(zlotowki)
    grosze = match.group('grosze')
    grosze = int(grosze) if grosze else 0
    return zlotowki + grosze / 100


if __name__ == '__main__':
    from bot.message import generate

    for promo in amso():
        print(generate(promo))
