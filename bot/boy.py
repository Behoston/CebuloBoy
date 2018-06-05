import argparse
import datetime
import logging
import time
from pprint import pprint

import telepot

import config
import models
from bot import message
from bot import scrapers

logger = logging.getLogger(__name__)


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


def wait_for_promotion(shop_name: str) -> models.Promotion or None:
    scrape = scrapers_map[args.action]
    start = datetime.datetime.now()
    timeout = datetime.timedelta(minutes=5)
    wait_time = datetime.timedelta(seconds=5)
    while start + timeout > datetime.datetime.now():
        promotion = scrape()
        last_promotion = models.Promotion.get_last(shop_name)
        if not last_promotion or (promotion and last_promotion.product_name != promotion.product_name):
            return promotion
        else:
            logging.warning("Promotion in {shop} not found. Waiting {wait}s...".format(
                shop=shop_name,
                wait=wait_time.total_seconds()),
            )
            time.sleep(wait_time.total_seconds())
            wait_time *= 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cebulo Boy main script')
    parser.add_argument(
        'action', type=str, choices={shop for shop in scrapers_map.keys()}.union({'update'}),
        help='service to scrape or print update to check `chat_id`')
    args = parser.parse_args()
    if args.action == 'update':
        get_update()
    elif args.action in scrapers_map:
        promotion = wait_for_promotion(args.action)
        if promotion:
            promotion.save()
            _message = message.generate(promotion)
            send_message(_message)
        else:
            logger.error("No promotion found for {}.".format(args.action))
    else:
        raise Exception
