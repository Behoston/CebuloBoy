import random

import models

greetings = [
    'Szanowni Państwo',
    'Wielmożni Państwo',
    'Witam',
    'Cześć',
    'Hej',
    'Z tej strony CebuloBoy',
    'Elo mordy',
    'Dzień dobry',
    'Witajcie',
    'Siema',
    'Czołem',
    'Piątka',
    'Żółwik',
    'Joł',
    'Ahoj',
    'Strzała',
]


def float_fucker(i: float) -> str:
    return str(round(i, 2)).strip('0').strip('.')


def generate(promotion: models.Promotion) -> str:
    code = 'Użyj kodu: `{}`\n'.format(promotion.code) if promotion.code else ''
    discount = promotion.old_price - promotion.new_price
    return (
        '{greetings}!\n'
        'Dziś w promocji mamy: *{product_name}*\n'
        'CENA: `{old_price} zł -> {new_price} zł`\n'
        '*Taniej o {discount} zł ({discount_percents}%)*\n'
        '{code}'
        '[Link do promocji]({url})'
    ).format(
        greetings=random.choice(greetings),
        product_name=promotion.product_name,
        old_price=float_fucker(promotion.old_price),
        new_price=float_fucker(promotion.new_price),
        discount=float_fucker(discount),
        discount_percents=float_fucker((discount / promotion.old_price) * 100),
        code=code,
        url=promotion.url,
    )
