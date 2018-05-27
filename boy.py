import argparse
import json
import re
from pprint import pprint

import lxml.html
import requests
import telepot

import config


def send_message(message):
    bot = telepot.Bot(config.TELEGRAM_TOKEN)
    bot.sendMessage(config.TELEGRAM_CHANNEL_ID, message, parse_mode='markdown')


def get_update():
    bot = telepot.Bot(config.TELEGRAM_TOKEN)
    pprint(bot.getUpdates())


def scrape(base_url: str) -> str:
    response = requests.get(base_url)
    tree = lxml.html.fromstring(response.text)
    hot_shot = tree.xpath('//div[@id="hotShot"]')[0]

    old_price = hot_shot.xpath('.//div[@class="old-price"]')[0].text
    new_price = hot_shot.xpath('.//div[@class="new-price"]')[0].text
    discount = hot_shot.xpath('.//span[@class="discount-value"]')[0].text
    product_name = hot_shot.xpath('.//p[@class="product-name"]')[0].text

    hot_shot_script = hot_shot.xpath('following-sibling::script')[0].text
    match = re.search(r'window\.location ?= ?(?P<link>.*);', hot_shot_script)
    url = json.loads(match.group('link'))
    return (
        'Elo mordy!\n'
        'Dziś w promocji mamy: *{product_name}*\n'
        'CENA: `{old_price} -> {new_price}`\n'
        '({discount})\n'
        '[Link do promocji]({base_url}{url})'
    ).format(
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        discount=discount,
        base_url=base_url,
        url=url,
    )


def morele() -> str:
    response = requests.get('https://www.morele.net/')
    tree = lxml.html.fromstring(response.text)
    promo = tree.xpath('//div[@class="promotion-product"]')[0]

    product_link = promo.xpath('.//div[@class="product-name"]/a')[0]
    product_name = product_link.text.strip()
    product_url = product_link.get('href')
    price = promo.xpath('.//div[@class="product-price"]')[0]
    old_price = price.xpath('.//div[contains(@class, "old")]/span')[0].text.strip()
    new_price = price.xpath('.//div[contains(@class, "new")]/span')[0].text.strip()
    code = promo.xpath('.//div[@class="product-code"]')[0].text.strip()

    return (
        'Witam!\n'
        'Dziś w promocji mamy: *{product_name}*\n'
        'CENA: `{old_price} -> {new_price}`\n'
        'KOD: `{code}`\n'
        '[Link do promocji]({product_url})'
    ).format(
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        code=code,
        product_url=product_url,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cebulo Boy main script')
    parser.add_argument(
        'action', type=str, choices={'alto', 'xkom', 'morele', 'update'},
        help='service to scrape or print update to check `chat_id`')
    args = parser.parse_args()
    message = None
    if args.action == 'alto':
        message = scrape('https://al.to')
    elif args.action == 'xkom':
        message = scrape('https://x-kom.pl')
    elif args.action == 'morele':
        message = morele()
    elif args.action == 'update':
        get_update()
    else:
        raise Exception
    if message:
        send_message(message)
