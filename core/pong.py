import wmi, os, pickle, subprocess
from colored import fg, stylize, attr

def ejecutar_icmp():
    os.system("python core/icmp.py")

def obtener_interfaz():
    # Se utiliza la API de Windows para obtener las interfaces de red
    interfaz = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
    return interfaz

def get_connection_status(interfaz):
    if not hasattr(interfaz, 'NetConnectionStatus'):
        return stylize("No disponible", fg("red"))
    status_code = interfaz.NetConnectionStatus
    status_dict = {
        0: "Desconectado",
        1: "Conectando",
        2: "Conectado",
        3: "Desconectando",
        4: "Desconectado",
        5: "Desconectado",
        6: "Autenticando",
        7: "Reconectando"
    }
    return status_dict.get(status_code, "Desconocido")

def imprimir_interfaz(interfaz):
    # Se limpia la pantalla
    os.system("cls")

    # Se imprimen los detalles de la interfaz seleccionada en el formato indicado
    print(f"{fg('green')}Interfaz: {fg('magenta')}{interfaz.Caption}{attr('reset')}")
    print(f"{fg('green')}Dirección IPv4: {fg('blue')}{interfaz.IPAddress[0]}{attr('reset')}")
    print(f"{fg('green')}Dirección IPv6: {fg('blue')}{interfaz.IPAddress[1]}{attr('reset')}")
    print(f"{fg('green')}MAC Address: {fg('blue')}{interfaz.MACAddress}{attr('reset')}")
    print(f"{fg('green')}Subnet Mask: {fg('blue')}{interfaz.IPSubnet[0]}{attr('reset')}")
    if hasattr(interfaz, 'Speed'):
        print(f"{fg('green')}Velocidad de conexión: {fg('blue')}{interfaz.Speed} Mbps{attr('reset')}")
    else:
        print(f"{fg('green')}Velocidad de conexión: {fg('red')}No disponible{attr('reset')}")
    print(f"{fg('green')}Estado de la conexión: {fg('blue')}{get_connection_status(interfaz)}{attr('reset')}")
    gateway = interfaz.DefaultIPGateway[0] if interfaz.DefaultIPGateway else stylize("No disponible", fg("red"))
    print(f"{fg('green')}Gateway: {fg('blue')}{gateway}{attr('reset')}\n")

def guardar_variables(interfaz):
    # Se guarda la información de la interfaz seleccionada en un diccionario
    variables = {
        "Interfaz": interfaz.Caption,
        "Direccion IPv4": interfaz.IPAddress[0],
        "Gateway": interfaz.DefaultIPGateway[0] if interfaz.DefaultIPGateway else "No disponible"
    }
    
    # Se devuelve el diccionario con las variables
    return variables


def main():
    while True:
        # Se limpia la pantalla
        os.system("cls")

        # Se obtienen y se imprimen las interfaces de red disponibles en magenta
        interfaces = obtener_interfaz()
        print("Interfaces disponibles:\n")
        for i, interfaz in enumerate(interfaces):
            print(f"{i+1}. {stylize(interfaz.Caption, fg('magenta'))}")

        # Se solicita al usuario que seleccione una interfaz en amarillo
        seleccion = input(stylize("\nSeleccione una interfaz o 'Q' para volver al menu principal: ", fg("yellow")))
        if seleccion == "Q":
            break

        # Se valida la entrada del usuario
        if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(interfaces):
            print("Selección inválida. Intente de nuevo.")
            continue
        # Se imprime la interfaz seleccionada
        interfaz_seleccionada = interfaces[int(seleccion)-1]
        imprimir_interfaz(interfaz_seleccionada)

        # Se guarda la información de la interfaz seleccionada en un diccionario
        variables = guardar_variables(interfaz_seleccionada)

        # Guardar el diccionario con las variables en un archivo binario
        with open("core/temp/variables.dat", "wb") as f:
            pickle.dump(variables, f)

        # Se le pregunta al usuario si quiere analizar otra interfaz o salir
        seleccion = input(stylize("Presione Enter para volver al menu de interfaces, 'Q' para salir o 'R' para escanear: ", fg("yellow")))
        if seleccion == "Q":
            break
        elif seleccion == "R":
            ejecutar_icmp()
            break
        
    print("¡Hasta pronto!")

if __name__ == "__main__":
    main()
