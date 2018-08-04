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

PROMOTION_PADDING = 5

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    style='{',
    format='[{asctime}]{levelname}:CEBULOBOT:{message}',
)


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
    'hard-pc': scrapers.hard_pc,
    'komputronik': scrapers.komputronik,
    'proline': scrapers.proline,
}


def wait_for_promotions(shop_name: str) -> [models.Promotion]:
    scrape_fn = scrapers_map[shop_name]
    start = datetime.datetime.now()
    # TODO: enable timeouts when async
    timeout = datetime.timedelta(seconds=5)
    wait_time = datetime.timedelta(seconds=0)
    while start + timeout > datetime.datetime.now():
        promotion = scrape_fn()
        if not promotion:
            logging.warning("Promotion in {} not found. Waiting {}s...".format(shop_name, wait_time.total_seconds()))
            time.sleep(wait_time.total_seconds())
            wait_time *= 2
        else:
            if not isinstance(promotion, list):
                promotions = [promotion]
            else:
                promotions = promotion
            i = PROMOTION_PADDING + len(promotions)
            last_promotions_names = {
                last_promotion.product_name
                for last_promotion
                in models.Promotion.get_last_x(shop_name, i)
            }
            result = []
            for promotion in promotions:
                if promotion.product_name not in last_promotions_names:
                    result.append(promotion)
            return result

    return []


time_schedule = {
    'komputronik': {1},
    'alto': {9, 21},
    'xkom': {10, 22},
    'proline': set(range(25)),
    'hard-pc': set(range(25)),
    'morele': set(range(25)),
}


def schedule_scraping():
    actual_hour = datetime.datetime.now().hour
    for shop, promotion_hours in time_schedule.items():
        if actual_hour in promotion_hours:
            scrape(shop)


def scrape(shop: str):
    logger.info("Looking for a promotion(s) in '{}'.".format(shop))
    promotions = wait_for_promotions(shop)
    for promotion in promotions:
        promotion.save()
        _message = message.generate(promotion)
        send_message(_message)
    if not promotions:
        logger.error("No promotion found for '{}'.".format(shop))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cebulo Boy main script')
    parser.add_argument(
        '--show-updates',
        action='store_true',
        help='prints updates to check `chat_id`',
    )
    args = parser.parse_args()
    if args.show_updates:
        get_update()
    else:
        schedule_scraping()
