from App import App

# Esta funcion espera la entrada de texto por el usuario y separa por espacios en blanco, retorna una lista con las palabras ingresadas.
def prompt() -> list[str]:
    text = input('\n> ')

    return text.split(' ')


def show_help():
    print('Por hacer: Aqui va un mensaje de ayuda')


def main():

    app = App('fca_live_kLDaZSlSucLjUTwctTPP7XLkTToRMDil2pfJpLuo')
    app.load_data()

    while True: # Bucle infinito para simular una terminal.

        text_input = prompt()
        command = text_input[0] # La primera palabra de la lista es el comando.

        if command == '':
            continue
        elif command == 'quit' or command == 'q': # Si el usuario ingresa "quit" o "q", sale del bucle y por ende del programa.
            break
        elif command == 'help' or command == '?':
            show_help()
        elif command == "conv":
            app.convert(float(text_input[1]), text_input[2], text_input[4].split(','))
        elif command == 'supported':
            app.supported_currencies()
        elif command == 'search':
            app.search_currency(text_input[1])
        else:
            print('Comando invalido. Por favor escriba "help" o "?" para obtener ayuda.')


if __name__ == '__main__':
    main()
