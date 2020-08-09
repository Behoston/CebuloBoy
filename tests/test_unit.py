import pytest

from bot import message
from bot import scrapers


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
    parsed_price = scrapers._price_parser(price)
    assert parsed_price == expected_value


@pytest.mark.parametrize(
    ('number', 'expected_sting'), [
        (100, '100'),
        (3.14159265359, '3.14'),
        (8.555, '8.56'),
        (1.001, '1'),
    ],
)
def test_float_fucker(number: float, expected_sting: str):
    number_string = message.float_fucker(number)
    assert number_string == expected_sting
