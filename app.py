import yaml
from sanic import Sanic
from sanic.response import json

import models

app = Sanic()


@app.route('/doc')
async def doc(request):
    with open('api.yml') as f:
        return json(yaml.load(f))


@app.route('/last_promotions')
async def last_promotions(request):
    shops = models.Shop.select()
    response = []
    for shop in shops:
        response.append({
            'name': shop.name,
            'last_promotions': [
                serialize_promotion(promotion)
                for promotion in shop.last_promotions(6)
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
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)
