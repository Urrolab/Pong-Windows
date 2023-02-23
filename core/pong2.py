import pickle
import os
import subprocess
from colored import fg, stylize, attr


DATOS_MAC_PATH = 'core/temp/macs.dat'
DATOS_VARIABLES_PATH = 'core/temp/variables.dat'


def cargar_datos(path):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"{fg('red')}ERROR: No se encontró el archivo de datos.{attr('reset')}")
        exit(1)
    except Exception as e:
        print(f"{fg('red')}ERROR al cargar los datos: {str(e)}{attr('reset')}")
        exit(1)


def imprimir_informacion_ip(ip, detalles):
    print(f"Detalles de la IP {fg('blue')}{ip}{attr('reset')}: \n")
    print(f"{fg('white')}MAC Address: {fg('red')}{detalles['mac_address']} {attr('reset')}({detalles['vendor']})\n")
    input(f"{fg('yellow')}Enter para continuar...")


def imprimir_ips(datos_mac):
    os.system("cls")
    variables = cargar_datos(DATOS_VARIABLES_PATH)
    print(f"{fg('magenta')}{variables['Interfaz']}{attr('reset')} IP's escaneadas:\n")
    for i, ip in enumerate(datos_mac.keys()):
        detalles = datos_mac[ip]
        if detalles['vendor'] == 'Desconocido':
            print(f"{fg('white')}{i+1}. {fg('blue')}{ip} {fg('white')}(MAC: {stylize(detalles['mac_address'], fg('red'))})")
        else:
            print(f"{fg('white')}{i+1}. {fg('blue')}{ip} {fg('white')}({detalles['vendor']})")


def seleccionar_ip(datos_mac):
    while True:
        imprimir_ips(datos_mac)
        choice = input(f"{fg('yellow')}\nSeleccione una IP para analizar puertos, 'Q' para salir, 'R' para re-escanear: {attr('reset')}")
        if choice == 'Q':
            subprocess.run(["python", "menu.py"])
        elif choice == 'R':
            subprocess.run[("python", "core/pong.py")]
        elif choice.isdigit() and int(choice) in range(1, len(datos_mac)+1):
            os.system("cls")
            ip = list(datos_mac.keys())[int(choice)-1]
            detalles = datos_mac[ip]
            imprimir_informacion_ip(ip, detalles)
        else:
            print(f"{fg('red')}Selección inválida. Por favor intente nuevamente.")
            input(f"{fg('yellow')}Presione Enter para continuar...")


def main():
    datos_mac = cargar_datos(DATOS_MAC_PATH)
    seleccionar_ip(datos_mac)


if __name__ == '__main__':
    main()
