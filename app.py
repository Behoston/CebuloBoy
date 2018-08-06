import yaml
from feedgen.feed import FeedGenerator
from sanic import Sanic
from sanic.response import HTTPResponse
from sanic.response import json

import models
from bot.message import float_fucker

app = Sanic()

DEFAULT_PROMOTION_LIMIT = 5
MAX_PROMOTION_LIMIT = 20


@app.route('/doc')
async def doc(request):
    with open('api.yml') as f:
        return json(yaml.load(f))


@app.route('/last_promotions')
async def last_promotions(request):
    shops = models.Shop.select()
    response = []
    limit = min(int(request.args.get('limit', DEFAULT_PROMOTION_LIMIT)), MAX_PROMOTION_LIMIT)
    for shop in shops:
        response.append({
            'name': shop.name,
            'last_promotions': [
                serialize_promotion(promotion)
                for promotion in shop.last_promotions(limit)
            ]
        })
    return json(response)


def serialize_promotion(promotion: models.Promotion) -> dict:
    return {
        'product_name': promotion.product_name,
        'old_price': promotion.old_price,
        'new_price': promotion.new_price,
        'url': promotion.url,
        'code': promotion.code,
        'timestamp': promotion.timestamp,
    }


@app.route('/rss')
async def rss(request):
    fg = FeedGenerator()
    fg.title('Cebulowy RSS')
    fg.id('https://cebul.ga')
    fg.link(href='https://cebul.ga/rss')
    fg.description("Najnowsze promocje ze sklepów z elektroniką użytkową.")
    shops = models.Shop.select()
    limit = min(int(request.args.get('limit', DEFAULT_PROMOTION_LIMIT)), MAX_PROMOTION_LIMIT)
    for shop in shops:
        for promotion in shop.last_promotions(limit):
            fe = fg.add_entry()
            fe.title(
                "[{new_price} PLN] {product_name}".format(
                    new_price=float_fucker(promotion.new_price),
                    product_name=promotion.product_name,
                )
            )
            fe.id(promotion.url)
            fe.link(href=promotion.url)
            code = '<br>Użyj kodu: <code>{}</code>'.format(promotion.code) if promotion.code else ''
            discount = promotion.old_price - promotion.new_price
            fe.description((
                'Dziś w promocji mamy: <b>{product_name}</b><br>'
                'CENA: {old_price} zł -> {new_price} zł<br>'
                '<b>Taniej o {discount} zł ({discount_percents}%)</b>'
                '{code}'
            ).format(
                product_name=promotion.product_name,
                old_price=float_fucker(promotion.old_price),
                new_price=float_fucker(promotion.new_price),
                discount=float_fucker(discount),
                discount_percents=float_fucker((discount / promotion.old_price) * 100),
                code=code,
            ))
    return HTTPResponse(fg.rss_str().decode('utf-8'), content_type='application/rss+xml')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)
