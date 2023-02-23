import pickle, os
from colored import fg, stylize, attr

def cargar_datos():
    with open('core/temp/macs.dat', 'rb') as f:
        return pickle.load(f)

def cargar_datos_variables():
    with open('core/temp/variables.dat', 'rb') as f:
        return pickle.load(f)

def imprimir_ips(macs):
    os.system("cls")
    variables = cargar_datos_variables()
    print(f"{fg('magenta')}{variables['Interfaz']}{attr('reset')} IP's escaneadas:\n")
    for i, ip in enumerate(macs.keys()):
        if macs[ip]['vendor'] == 'Desconocido':
            print(f"{fg('white')}{i+1}. {fg('blue')}{ip} {fg('white')}(MAC: {stylize(macs[ip]['mac_address'], fg('red'))})")
        else:
            print(f"{fg('white')}{i+1}. {fg('blue')}{ip} {fg('white')}({macs[ip]['vendor']})")

def seleccionar_ip(macs):
    while True:
        imprimir_ips(macs)
        choice = input(f"{fg('yellow')}\nSeleccione una IP para analizar puertos (o presione 'q' para salir): {attr('reset')}")
        if choice == 'q':
            break
        elif choice.isdigit() and int(choice) in range(1, len(macs)+1):
            os.system("cls")
            ip = list(macs.keys())[int(choice)-1]
            details = macs[ip]
            print(f"Detalles de la IP {fg('red')}{ip}{attr('reset')}: \n")
            print(f"{fg('green')}MAC Address: {fg('blue')}{details['mac_address']} {attr('reset')}({details['vendor']})\n")
            input("Presione Enter para continuar...")
        else:
            print("Selección inválida. Por favor intente nuevamente.")
            input("Presione Enter para continuar...")

def main():
    macs = cargar_datos()
    seleccionar_ip(macs)

if __name__ == '__main__':
    main()

