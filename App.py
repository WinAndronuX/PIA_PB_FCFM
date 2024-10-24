import json
import os.path
import freecurrencyapi

class App:

    def __init__(self, api_key: str):
        
        self.api = freecurrencyapi.Client(api_key)
        self.currencies = {}
        self.exchanges = {}

    def load_data(self):
        # Manejo de errores con estructura try
        try:
            currencies_path = 'data/currencies.json'

            if os.path.exists(currencies_path):
                with open(currencies_path, 'r') as f:
                    data = json.load(f)
                    self.currencies = data['data']

            else:
                os.mkdir('data')

                data = self.api.currencies()
                
                self.currencies = data['data']

                with open(currencies_path, 'w') as f:
                    json.dump(data, f)
                    f.close()
        # En caso de que la carpeta "data" ya exista, pero no contenga el archivo "currencies", se dara un error de tipo "FileExistsError"
        # El error "FileExistsError" puede suceder si antes existe un error de "Excpetion"
        except FileExistsError:
            print("No se puede crear un archivo que ya existe, por favor borra la carpeta data y vuelve a internarlo")
        # En caso de no tener conexion wifi o de haber algun error en el token del Api, se dara un error tipo "Exception"
        except Exception as e:
            print(f'Hay un error en el servidor, revisa tu token o tu conexion a internet')

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
            if response[0] == 'API returned errors:':
                raise ValueError("La moneda base es invalida")
            self.exchanges[base_currency] = response['data']

        return self.exchanges[base_currency][target_currency]

    def convert(self, amount: float, base_currency: str, currencies: list[str]):
        # Manejo de errores con estructura try
        try: 
            for currency in currencies:

                result = self.get_exchange_rate(base_currency, currency) * amount

                print(f'{self.currencies[currency]['name']} ({self.currencies[currency]['code']}) -> '
                    f'{result:.2f} {self.currencies[currency]['symbol_native']}')
        # En caso de que la moneda a la que se quiere convertir no sea valida el tipo de error sea "KeyError"
        except KeyError:
            print('La moneda o monedas a las que quieres convertir no estan registradas')
        # En caso de que la moneda base no sea valida el tipo de error sea "Excepction"
        except Exception as e:
            print(f'Ha ocurrido un error: {e.args[1]['base_currency']}')