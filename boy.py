import argparse
import json
import re
from pprint import pprint

import lxml.html
import requests
import telepot

TOKEN = NotImplemented  # generate token here: https://telegram.me/BotFather
CHANNEL_ID = -99999999  # add bot to channel, send some message, then get update and find chat_id


def send_message(message):
    bot = telepot.Bot(TOKEN)
    bot.sendMessage(CHANNEL_ID, message, parse_mode='markdown')


def get_update():
    bot = telepot.Bot(TOKEN)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cebulo Boy main script')
    parser.add_argument(
        'action', type=str, choices={'alto', 'xkom', 'update'},
        help='service to scrape or print update to check `chat_id`')
    args = parser.parse_args()
    message = None
    if args.action == 'alto':
        message = scrape('https://al.to')
    elif args.action == 'xkom':
        message = scrape('https://x-kom.pl')
    elif args.action == 'update':
        get_update()
    else:
        raise Exception
    if message:
        send_message(message)
