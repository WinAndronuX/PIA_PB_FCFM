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


def validate_stats_syntax(text):
    date_pattern = r'(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])'
    pattern = r'^[a-zA-Z]{3}\s+vs\s[a-zA-Z]{3}(,[a-zA-Z]{3})*\s+start_date\s+' + date_pattern + r'\s+end_date\s+' + date_pattern + r'$'
    return re.match(pattern, text)


def welcome_message():
    return 'Bienvenido. Porfavor escriba "help" o "?" para recibir ayuda sobre como usar el programa.'

def show_help():
    print('''Mensaje de Ayuda
    
    conv:       Convierte de una divisa a otra
                
                Uso: conv [monto] [moneda base] to [moneda/s objetivo]
                Ejemplos de uso:
                    - conv 1 USD to MXN
                    - conv 1 EUR to USD,MXN,JPY
    
    stats:      Calcula el porcentaje de cambio (devaluacion) de una moneda frente a otra
                
                Uso: stats [moneda base] vs [moneda/s objetivo] start_date [formato: YYYY-MM-DD] end_date [formato: YYYY-MM-DD]
                Ejemplos de uso:
                    - stats USD vs MXN,JPY,EUR start_date 2023-01-01 end_date 2023-12-31
    
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
    try:
        app.load_data()
    except everapi.exceptions.IncorrectApikey:
        print('API Error: API KEY Incorrecta')
    except Exception as e:
            print('Program Error: '+ str(e))

    print(welcome_message())

    while True: # Bucle infinito para simular una terminal.

        text_input = prompt()
        command = text_input[0] # La primera palabra de la lista es el comando.

        try:            

            if command == '':
                continue
            elif command == 'quit' or command == 'q': # Si el usuario ingresa "quit" o "q", sale del bucle y por ende del programa.
                if app.historial["comandos"] == {}:
                    break
                else:
                    export = input("¿Quieres exportar el historial de hoy? S - Si, N - No \n \n >").upper()
                    if export == "S":
                        app.export_Historial()
                    break
            elif command == 'help' or command == '?':
                show_help()
                app.save_command(" ".join(text_input))
            elif command == "conv":
                if validate_conv_syntax(' '.join(text_input[1:])):
                    res = app.convert(float(text_input[1]), text_input[2].upper(), text_input[4].upper().split(',')) # Convertimos las monedas automaticamente a mayusculas
                    app.save_command(" ".join(text_input), res)
                else:
                    print('Sintaxis incorrecta. Por favor escriba "help" o "?" para mostrar ayuda.')
            elif command == 'stats':
                if validate_stats_syntax(' '.join(text_input[1:])):
                    res = app.stats(text_input[1], text_input[3].split(','), text_input[5], text_input[7])
                    app.save_command(" ".join(text_input), res)
                else:
                    print('Sintaxis incorrecta. Por favor escriba "help" o "?" para mostrar ayuda.')
            elif command == 'supported':
                res = app.supported_currencies()
                app.save_command(" ".join(text_input), res)
            elif command == 'search':
                res = app.search_currency(text_input[1])
                app.save_command(" ".join(text_input), res)
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
