import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class ValueConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Неудалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Неудалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неудалось обработать количество {amount}')

        r = requests.get(f'https://api.coingate.com/v2/rates/merchant/{quote_ticker}/{base_ticker}')
        total_base = amount * float(json.loads(r.content))

        return total_base
