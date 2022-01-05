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
    end_date = peewee.DateTimeField(null=True, index=True, default=None)
    items_available = peewee.IntegerField(null=True, default=None)
    items_sold = peewee.IntegerField(null=True, default=None)

    @property
    def items_total(self) -> int:
        if self.items_available:
            return self.items_available + self.items_sold

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
            '{code}'
            '{number_of_items})').format(
            shop_name=self.shop,
            product_name=self.product_name,
            old_price=self.old_price,
            new_price=self.new_price,
            url=self.url,
            code=self.code,
            number_of_items=self.number_of_items,
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

    @classmethod
    def get_last_x(cls, shop: str, x: int):
        return cls.select().join(
            Shop
        ).where(
            Shop.name == shop
        ).order_by(
            Promotion.timestamp.desc()
        ).limit(x)


if __name__ == '__main__':
    from playhouse.migrate import SqliteMigrator, migrate

    db.connect()
    db.create_tables([Shop, Promotion])
    Shop.insert_many([
        {'name': 'xkom'},
        {'name': 'alto'},
        {'name': 'morele'},
        {'name': 'hard-pc'},
        {'name': 'komputronik'},
        {'name': 'proline'},
        {'name': 'wlodipol'},
        {'name': 'zadowolenie'},
        {'name': 'combat'},
        {'name': 'amso'},
    ]).on_conflict_ignore().execute()
    migrator = SqliteMigrator(db)
    # TODO: improve migrations!
    migrations = [
        # Add date when promotion ends and add number of items in promotion
        migrator.add_column('promotion', 'end_date', peewee.DateTimeField(default=None, null=True)),
        migrator.add_index('promotion', 'end_date'),
        migrator.add_column('promotion', 'number_of_items', peewee.IntegerField(default=None, null=True)),
        # Redesign items counts
        migrator.rename_column('promotion', 'number_of_items', 'items_available'),
        migrator.add_column('promotion', 'items_sold', peewee.IntegerField(default=None, null=True)),
    ]
    for migration in migrations:
        try:
            migrate(migration)
        except peewee.OperationalError:
            pass
