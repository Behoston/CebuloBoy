import argparse
from pprint import pprint

import telepot

import config
from bot import message
from bot import scrapers


def send_message(message: str):
    bot = telepot.Bot(config.TELEGRAM_TOKEN)
    bot.sendMessage(config.TELEGRAM_CHANNEL_ID, message, parse_mode='markdown')


def get_update():
    bot = telepot.Bot(config.TELEGRAM_TOKEN)
    pprint(bot.getUpdates())


scrapers_map = {
    'xkom': scrapers.xkom,
    'alto': scrapers.alto,
    'morele': scrapers.morele,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cebulo Boy main script')
    parser.add_argument(
        'action', type=str, choices={shop for shop in scrapers_map.keys()}.union({'update'}),
        help='service to scrape or print update to check `chat_id`')
    args = parser.parse_args()
    if args.action == 'update':
        get_update()
    elif args.action in scrapers_map:
        promotion = scrapers_map[args.action]()
        promotion.save()
        _message = message.generate(promotion)
        send_message(_message)
    else:
        raise Exception
