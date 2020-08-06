import models


def float_fucker(i: float) -> str:
    return str(round(i, 2)).strip('0').strip('.')


def generate(promotion: models.Promotion) -> str:
    code = '🗝 Użyj kodu: `{}`\n'.format(promotion.code) if promotion.code else ''
    if promotion.end_date is not None:
        date = promotion.end_date.strftime('%d-%m-%Y')
        time = promotion.end_date.strftime('%H:%M:%S')
        end_date = '\n⏰ Promocja trwa do {} dnia {}'.format(time, date)
    else:
        end_date = ''
    if promotion.items_available:
        number_of_items = '\n📦 Sztuk w promocji: {}'.format(promotion.items_total)
    else:
        number_of_items = ''
    discount = promotion.old_price - promotion.new_price
    return (
        '🧅 *{product_name}*\n'
        '💵 {old_price} zł -> {new_price} zł\n'
        '📉 *Taniej o {discount} zł ({discount_percents}%)*\n'
        '{code}'
        '🔗 [Link do promocji]({url})'
        '{number_of_items}'
        '{end_date}'
    ).format(
        product_name=promotion.product_name,
        old_price=float_fucker(promotion.old_price),
        new_price=float_fucker(promotion.new_price),
        discount=float_fucker(discount),
        discount_percents=float_fucker((discount / promotion.old_price) * 100),
        code=code,
        url=promotion.url,
        number_of_items=number_of_items,
        end_date=end_date,
    )
