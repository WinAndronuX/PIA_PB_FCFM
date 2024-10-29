import json
import os.path
from datetime import datetime
import freecurrencyapi

class App:

    def __init__(self, api_key: str):
        self.api = freecurrencyapi.Client(api_key)
        self.currencies = {}
        self.exchanges = {}
        self.historical = {}

    def load_data(self):
        currencies_path = 'data/currencies.json'

        if os.path.exists(currencies_path):
            with open(currencies_path, 'r') as f:
                data = json.load(f)
                self.currencies = data['data']

        else:
            if not os.path.exists('data'):
                os.mkdir('data')

            data = self.api.currencies()
            self.currencies = data['data']

            with open(currencies_path, 'w') as f:
                json.dump(data, f)
                f.close()

    def supported_currencies(self):

        for code, currency in self.currencies.items():
            print(f'{code}: [{currency['symbol_native']}] - {currency['name']}')

    def search_currency(self, text: str):

        for code, currency in self.currencies.items():
            name: str = currency['name']

            if text.lower() in name.lower():
                print(f'{code}: [{currency['symbol_native']}] - {currency['name']}')

    def get_exchange_rate(self, base_currency: str, target_currency: str) -> float:

        if base_currency not in self.exchanges:

            response = self.api.latest(base_currency)
            self.exchanges[base_currency] = response['data']

        return self.exchanges[base_currency][target_currency]

    def get_historical_exchange_rate(self, base_currency: str, target_currency: str, date: str) -> float:

        if datetime.now().strftime('%Y-%m-%d') == date:
            return self.get_exchange_rate(base_currency, target_currency)
        else:

            if date not in self.historical:
                self.historical[date] = {}

            if base_currency not in self.historical[date]:

                response = self.api.historical(date, base_currency)
                self.historical[date][base_currency] = response['data'][date]

            return self.historical[date][base_currency][target_currency]

    def convert(self, amount: float, base_currency: str, currencies: list[str]):

        if base_currency not in self.currencies.keys():
            print('Codigo de moneda base invalido: ' + base_currency)
            return

        for currency in currencies:

            if currency not in self.currencies.keys():
                print('Codigo de moneda objetivo invalido: ' + currency)
                return

            result = self.get_exchange_rate(base_currency, currency) * amount

            print(f'{self.currencies[currency]['name']} ({self.currencies[currency]['code']}) -> '
                  f'{result:.2f} {self.currencies[currency]['symbol_native']}')
