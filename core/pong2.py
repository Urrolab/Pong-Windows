import pickle
import os
import subprocess
import os.path
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
    while True:
        print(f"Detalles de la IP {fg('blue')}{ip}{attr('reset')}: \n")
        print(f"{fg('white')}MAC Address: {fg('red')}{detalles['mac_address']} {attr('reset')}({detalles['vendor']})\n")
        
        # Verifica si el archivo con el nombre de la IP existe
        archivo_ip = f"{ip}.dat"
        if os.path.isfile(archivo_ip):
            # Si el archivo existe, lo carga y obtiene los puertos abiertos
            with open(archivo_ip, "rb") as f:
                puertos_abiertos = pickle.load(f)
        else:
            # Si el archivo no existe, establece los puertos abiertos como una lista vacía
            puertos_abiertos = []
        
        # Agrega la información de los puertos a la cadena de salida
        if puertos_abiertos:
            print(f"Puertos: {puertos_abiertos}\n")
        else:
            print(f"Puertos: [0]\n")
        
        # Pide al usuario que ingrese una opción
        opcion = input(f"{fg('yellow')}Enter para escanear, 'Q' para salir, 'R' para buscar otra IP: {attr('reset')}")
        if opcion.lower() == 'q':
            subprocess.run(["python", "menu.py"])
        elif opcion.lower() == 'r':
            subprocess.run(["python", "core/pong2.py"])
        else:
            subprocess.run(["python", "core/ports.py"])

def imprimir_ips(datos_mac):
    os.system("cls")
    variables = cargar_datos(DATOS_VARIABLES_PATH)
    print(f"{fg('magenta')}{variables['Interfaz']}{attr('reset')} IP's escaneadas:\n")
    for i, ip in enumerate(datos_mac.keys()):
        detalles = datos_mac[ip]
        if detalles['vendor'] == 'Desconocido':
            print(f"{fg('white')}{i+1}. {fg('blue')}{ip} {fg('white')}(MAC: {stylize(detalles['mac_address'], fg('red'))})", end="")
        else:
            print(f"{fg('white')}{i+1}. {fg('blue')}{ip} {fg('white')}({detalles['vendor']})", end="")
        
        # Comprobar si existe un archivo con el nombre de la IP
        filename = os.path.join("core", "temp", f"{ip}.dat")
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                puerto_count = len(pickle.load(f))
            print(f" (Puertos escaneados: {fg('red')}{puerto_count}{attr('reset')})", end="")
        else:
            print(f" (Puertos escaneados: {fg('red')}0{attr('reset')})", end="")
            
        print("")

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
