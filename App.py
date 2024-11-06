import json
import os.path
from datetime import datetime
import freecurrencyapi
from openpyxl import Workbook

def devaluation_rate(initial_value, end_value):
    percentage_of_change = ((end_value - initial_value) / initial_value) * 100
    return percentage_of_change


class App:

    def __init__(self, api_key: str):
        self.api = freecurrencyapi.Client(api_key)
        self.currencies = {}
        self.exchanges = {}
        self.historical = {}
        self.historial = {"fecha": datetime.now().strftime("%d/%m/%Y"), "comandos": {}}

    def save_command(self, command, result = ""):
        self.historial["comandos"][datetime.now().strftime("%H:%M:%S")] = (command, result)
        pass

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

        resArray = []

        for code, currency in self.currencies.items():
            res = (f'{code}: [{currency['symbol_native']}] - {currency['name']}')
            print(res)
            resArray.append(res)
        
        return resArray

    def search_currency(self, text: str):
        
        resArray = []

        for code, currency in self.currencies.items():
            name: str = currency['name']

            if text.lower() in name.lower():
                res = (f'{code}: [{currency['symbol_native']}] - {currency['name']}')
                print(res)
                resArray.append(res)

        return resArray

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

        resArray = []

        if base_currency not in self.currencies.keys():
            res = ('Codigo de moneda base invalido: ' + base_currency)
            print(res)
            return res

        for currency in currencies:

            if currency not in self.currencies.keys():
                res = ('Codigo de moneda objetivo invalido: ' + currency)
                print(res)
                return res

            result = self.get_exchange_rate(base_currency, currency) * amount

            res = (f'{self.currencies[currency]['name']} ({self.currencies[currency]['code']}) -> '
                f'{result:.2f} {self.currencies[currency]['symbol_native']}')

            resArray.append(res)
            
            print(res)

        return resArray

    def stats(self, base_currency: str, currencies: list[str], initial_date: str, end_date: str):

        date1 = datetime.strptime(initial_date, '%Y-%m-%d').date()
        date2 = datetime.strptime(end_date, '%Y-%m-%d').date()

        if date2 < date1:
            res ='end_date no puede ser menor que start_date'
            print(res)
            return res
        elif date1 == date2:
            res ='start_date y end_date no pueden ser iguales'
            print(res)
            return res
        elif date2 > datetime.now().date():
            res = 'end_date no puede ser mayor que el dia actual'
            print(res)
            return res

        if base_currency not in self.currencies.keys():
            res = 'Codigo de moneda base invalido: ' + base_currency
            print(res)
            return res

        resArray = []

        for currency in currencies:
            
            if currency not in self.currencies.keys():
                res = 'Codigo de moneda base invalido: ' + base_currency
                print(res)
                return res

            exchange1 = self.get_historical_exchange_rate(base_currency, currency, initial_date)
            exchange2 = self.get_historical_exchange_rate(base_currency, currency, end_date)

            result = devaluation_rate(exchange1, exchange2)

            res = (f'''{self.currencies[currency]['name']} ({self.currencies[currency]['code']}):
    Exchange rate at {initial_date}: {exchange1:.2f} {self.currencies[currency]['symbol_native']}
    Exchange rate at {end_date}: {exchange2:.2f} {self.currencies[currency]['symbol_native']}
    Devaluation: {result:+.2f} %''')
            
            print(res)

            resArray.append(res)

        return resArray

    def export_Historial(self):

        wb = Workbook()

        hoja = wb.active

        hoja.title = f'Historial {datetime.now().strftime("%d-%m-%Y")}'
        hoja['A1'] = "Hora"
        hoja['B1'] = "Comando"
        hoja['C1'] = "Resultado"

        i = 2

        for clave, valor in self.historial["comandos"].items():
            hoja[f'A{i}'] = clave
            hoja[f'B{i}'] = valor[0]
            if isinstance(valor[1], list):
                for element in valor[1]:
                    hoja[(f'C{i}')] = element
                    i += 1
            elif isinstance(valor[1], str):
                hoja[(f'C{i}')] = valor[1]
                i += 1
            else:
                print("Error")
            
            i += 1

        wb.save("Historial.xlsx")