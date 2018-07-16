import pytest

from bot.scrapers import _price_parser


@pytest.mark.parametrize(
    ('price', 'expected_value'), [
        # separators
        ('1500', 1500),
        ('1500PLN', 1500),
        ('1500 PLN', 1500),
        ('1500zł', 1500),
        ('1 500zł', 1500),
        ('1\u00a0500zł', 1500),
        ('1\t500zł', 1500),
        ('1\n500zł', 1500),
        ('1 500 zł', 1500),
        ('1 500.00 zł', 1500),
        ('1 500. 00 zł', 1500),
        ('1 500 . 00 zł', 1500),
        ('1 500 .00 zł', 1500),
        ('1 500 ,00 zł', 1500),
        ('1 500 , 00 zł', 1500),
        ('1 500, 00 zł', 1500),
        # With grosze :P
        ('1,24', 1.24),
        ('1,24 zł', 1.24),
        ('1.24 zł', 1.24),
        ('1 , 24 zł', 1.24),
        ('1 . 24 zł', 1.24),
        ('1 .24 zł', 1.24),
        ('1\t.\t24 zł', 1.24),
    ])
def test_price_parser(price: str, expected_value):
    parsed_price = _price_parser(price)
    assert parsed_price == expected_value
