import argparse
import datetime
import logging
import os
import time
import typing
from pprint import pprint

import telepot

import config
import models
from bot import message, scrapers

PROMOTION_PADDING = int(os.getenv('PROMOTION_PADDING', '5'))

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    style='{',
    format='[{asctime}]{levelname}:CEBULOBOT:{message}',
)


def send_message(message: str):
    bot = telepot.Bot(config.TELEGRAM_TOKEN)
    bot.sendMessage(config.TELEGRAM_CHANNEL_ID, message, parse_mode='markdown')


def send_error(error):
    if config.TELEGRAM_ERROR_ID is not None:
        bot = telepot.Bot(config.TELEGRAM_TOKEN)
        bot.sendMessage(config.TELEGRAM_ERROR_ID, str(error))


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
    'zadowolenie': scrapers.zadowolenie,
    'combat': scrapers.combat,
}


def scrape(shop: str):
    logger.info("Looking for a promotion(s) in '{}'.".format(shop))
    promotions = wait_for_promotions(shop)
    for promotion in promotions:
        promotion.save()
        _message = message.generate(promotion)
        send_message(_message)
    if not promotions:
        error_message = "No promotion found for '{}'.".format(shop)
        logger.info(error_message)


def wait_for_promotions(shop_name: str) -> typing.List[models.Promotion]:
    scrape_fn = scrapers_map[shop_name]
    start = datetime.datetime.now()
    timeout = datetime.timedelta(minutes=5)
    wait_time = datetime.timedelta(seconds=5)
    while start + timeout > datetime.datetime.now():
        try:
            promotion = scrape_fn()
        except Exception as e:
            error_message = f"Scrape failed for shop {shop_name}! {e}"
            logger.error(error_message)
            send_error(error_message)
            promotion = None
        if promotion:
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
            if result:
                return result
        logging.warning("Promotion in {} not found. Waiting {}s...".format(shop_name, wait_time.total_seconds()))
        time.sleep(wait_time.total_seconds())
        wait_time *= 2
    return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cebulo Boy main script')
    parser.add_argument(
        '--shop',
        type=str,
        choices=scrapers_map.keys(),
        help="Shop sto scrape promotion.",
    )
    parser.add_argument(
        '--show-updates',
        action='store_true',
        help='prints updates to check `chat_id`',
    )
    args = parser.parse_args()
    if args.show_updates:
        get_update()
    elif args.shop:
        scrape(args.shop)
    else:
        raise Exception("--shop or --show-updates required!")
