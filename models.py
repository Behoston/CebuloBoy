import abc
import sqlite3

db = sqlite3.connect('database.sqlite3')


class Model(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def create_table(cls):
        pass

    @abc.abstractmethod
    def save(slef) -> int:
        pass


class Shop(Model):
    def __init__(self, name: str):
        self.name = name

    @classmethod
    def create_table(cls):
        db.execute("""
          CREATE TABLE IF NOT EXISTS shop (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL UNIQUE
          );
        """)
        db.commit()

    def save(self) -> int:
        cursor = db.execute("""
          INSERT OR IGNORE INTO shop (name) VALUES ('{name}')
        """.format(name=self.name))
        db.commit()
        return cursor.lastrowid

    @classmethod
    def get_id_by_name(cls, name: str) -> int:
        cursor = db.execute("""SELECT id FROM shop WHERE name=?""", [name])
        shop = cursor.fetchone()
        return shop[0]


class Promotion(Model):
    def __init__(
            self,
            shop_name: str,
            product_name: str,
            old_price: float,
            new_price: float,
            url: str,
            code: str or None = None,
    ):
        self.shop_name = shop_name
        self.product_name = product_name
        self.old_price = old_price
        self.new_price = new_price
        self.url = url
        self.code = code

    def __str__(self):
        return (
            'Promotion('
            '{shop_name}, '
            '{product_name}, '
            '{old_price}, '
            '{new_price}, '
            '{url}, '
            '{code})').format(
            shop_name=self.shop_name,
            product_name=self.product_name,
            old_price=self.old_price,
            new_price=self.new_price,
            url=self.url,
            code=self.code,
        )

    @classmethod
    def create_table(cls) -> int:
        cursor = db.execute("""
          CREATE TABLE IF NOT EXISTS promotion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            old_price FLOAT NOT NULL,
            new_price FLOAT NOT NULL,
            url TEXT NOT NULL,
            code VARCHAR(255) NULL DEFAULT NULL,
            datetime TEXT DEFAULT DATETIME('now'),
            FOREIGN KEY (shop_id) REFERENCES shop(id)
        );
        """)
        db.commit()
        return cursor.lastrowid

    def save(self) -> int:
        shop_id = Shop.get_id_by_name(self.shop_name)
        cursor = db.execute("""
          INSERT INTO promotion 
          (shop_id, product_name, old_price, new_price, url, code) 
          VALUES (?, ?, ?, ?, ?, ?)
        """, [shop_id, self.product_name, self.old_price, self.new_price, self.url, self.code])
        db.commit()
        return cursor.lastrowid


if __name__ == '__main__':
    Shop.create_table()
    Shop('alto').save()
    Shop('xkom').save()
    Shop('morele').save()
    Promotion.create_table()
