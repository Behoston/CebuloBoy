from datetime import datetime

import peewee

from config import DB_FILE

db = peewee.SqliteDatabase(DB_FILE)


class Shop(peewee.Model):
    name = peewee.CharField(unique=True)

    class Meta:
        database = db

    @classmethod
    def get_by_name(cls, name: str) -> int:
        return cls.get(Shop.name == name)

    def __str__(self):
        return 'Shop({name})'.format(name=self.name)


class Promotion(peewee.Model):
    shop = peewee.ForeignKeyField(Shop)
    product_name = peewee.CharField()
    old_price = peewee.FloatField()
    new_price = peewee.FloatField()
    url = peewee.CharField()
    code = peewee.CharField(null=True)
    timestamp = peewee.DateTimeField(default=datetime.now, index=True)

    def __init__(self, *args, **kwargs):
        if 'shop' in kwargs and isinstance(kwargs['shop'], str):
            kwargs['shop'] = Shop.get(name=kwargs['shop'])
        super().__init__(*args, **kwargs)

    class Meta:
        database = db

    def __str__(self):
        return (
            'Promotion('
            '{shop_name}, '
            '{product_name}, '
            '{old_price}, '
            '{new_price}, '
            '{url}, '
            '{code})').format(
            shop_name=self.shop,
            product_name=self.product_name,
            old_price=self.old_price,
            new_price=self.new_price,
            url=self.url,
            code=self.code,
        )

    @classmethod
    def get_last(cls, shop: str):
        return cls.select().join(
            Shop
        ).where(
            Shop.name == shop
        ).order_by(
            Promotion.timestamp.desc()
        ).first()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Shop, Promotion])
    Shop.insert_many([
        {'name': 'xkom'},
        {'name': 'alto'},
        {'name': 'morele'},
        {'name': 'hard-pc'},
        {'name': 'komputronik'},
    ]).on_conflict_ignore().execute()
