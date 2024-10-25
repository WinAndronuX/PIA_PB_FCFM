import everapi.exceptions
import requests

from App import App
import re

# Esta funcion espera la entrada de texto por el usuario y separa por espacios en blanco, retorna una lista con las palabras ingresadas.
def prompt() -> list[str]:
    text = input('\n> ')

    return text.split(' ')


# Funcion que recibe el patron, usando regex, que debe de tener el texto despues del comando "conv" para funcionar
def validate_conv_syntax(text):
    pattern = r"^\d+\s[a-zA-Z]{3}\sto\s[a-zA-Z]{3}(,[a-zA-Z]{3})*$"
    return re.match(pattern, text)


def show_help():
    print('''Mensaje de Ayuda
    
    conv:       Convierte de una divisa a otra
                
                Uso: conv [monto] [moneda base] to [moneda/s objetivo]
                Ejemplos de uso:
                    - conv 1 USD to MXN
                    - conv 1 EUR to USD,MXN,JPY
    
    supported:  Muestra todas las monedas disponibles, su nombre, simbolo y codigo
    
    search:     Muestra todas las monedas que coincidan con un parametro de busqueda
                
                Uso: search [texto a buscar]
                Ejemplos de uso:
                    - search peso
                    - search dollar
    
    help,?:     Muestra este mensaje de ayuda
    
    quit,q:     Sale del programa''')


def main():

    app = App('fca_live_kLDaZSlSucLjUTwctTPP7XLkTToRMDil2pfJpLuo')
    app.load_data()

    while True: # Bucle infinito para simular una terminal.

        text_input = prompt()
        command = text_input[0] # La primera palabra de la lista es el comando.

        try:

            if command == '':
                continue
            elif command == 'quit' or command == 'q': # Si el usuario ingresa "quit" o "q", sale del bucle y por ende del programa.
                break
            elif command == 'help' or command == '?':
                show_help()
            elif command == "conv":
                if validate_conv_syntax(' '.join(text_input[1:])):
                    app.convert(float(text_input[1]), text_input[2].upper(), text_input[4].upper().split(',')) # Convertimos las monedas automaticamente a mayusculas
                else:
                    print('Sintaxis incorrecta. Por favor escriba "help" o "?" para mostrar ayuda.')
            elif command == 'supported':
                app.supported_currencies()
            elif command == 'search':
                app.search_currency(text_input[1])
            else:
                print('Comando invalido. Por favor escriba "help" o "?" para obtener ayuda.')

        except requests.exceptions.ConnectionError:
            print('System Error: Por favor verifique su conexion a internet.')
        except everapi.exceptions.IncorrectApikey:
            print('API Error: API KEY Incorrecta')
        except everapi.exceptions.QuotaExceeded:
            print('API Error: Cuota excedida')
        except everapi.exceptions.RateLimitExceeded:
            print('API Error: Limite de consultas excedido')
        except everapi.exceptions.ApiError as e:
            print('API Error: ' + str(e))
        except Exception as e:
            print('Program Error: '+ str(e))


if __name__ == '__main__':
    main()
