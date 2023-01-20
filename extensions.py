import requests
import json
from config import currency, headers

class APIException(Exception):
    pass

class CurrencyConverter:

    """Пример вывода при запросе  res = {'success': True, 'query': {'from': 'USD', 'to': 'RUB', 'amount': 10},
          'info': {'timestamp': 1673617023, 'rate': 68.628033}, 'date': '2023-01-13', 'result': 686.28033}"""

    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Нельзя конвертировать из "{currency[quote]}" в "{currency[base]}"')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException('Колличество не может быть отрицательным')
        except ValueError:
            raise APIException(f'Не удалось обработать колличество "{amount}"')


        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"

        payload = {}

        response = requests.request("GET", url, headers=headers, data = payload)

        res = json.loads(response.content)

        total = res['result']
        rate = res['info']['rate']

        return total, rate
