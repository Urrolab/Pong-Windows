import subprocess, os, pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
from colored import fg, stylize, attr

def cargar_variables(nombre_archivo):
    """Carga las variables almacenadas en un archivo utilizando el módulo pickle."""
    nombre_archivo = 'core/temp/variables.dat'
    with open(nombre_archivo, 'rb') as f:
        variables = pickle.load(f)
    return variables

def mostrar_informacion(interfaz, ipv4, gateway):
    """Muestra información sobre la interfaz, la dirección IPv4 y el gateway."""
    os.system("cls")
    print(f"{fg('white')}Interfaz: {fg('magenta')}{interfaz}{attr('reset')}")
    print(f"{fg('white')}IPv4: {fg('blue')}{ipv4}{attr('reset')}")
    print(f"{fg('white')}Gateway: {fg('blue')}{gateway}{attr('reset')}")

def ping(ip):
    """Ejecuta el comando ping para la dirección IP dada y devuelve el código de retorno."""
    proceso_ping = subprocess.run(['ping', '-n', '1', '-w', '500', ip], capture_output=True)
    return ip, proceso_ping.returncode

def escanear_ips(gateway):
    """Realiza un ping a todas las direcciones IP en el rango de la red local
    que se encuentra detrás del gateway proporcionado utilizando hilos."""
    if gateway == "No disponible":
        print(f"{fg('red')}\nNo se puede realizar un escaneo sobre una interfaz sin Gateway{attr('reset')}")
        input(f"{fg('yellow')}\nEnter para volver al menu de interfaces.{attr('reset')}")
        return
    # Obtener los octetos de la dirección IP del gateway
    octetos_gateway = gateway.split('.')
    
    # Generar las direcciones IP para escanear
    ips = [f"{octetos_gateway[0]}.{octetos_gateway[1]}.{octetos_gateway[2]}.{i}" for i in range(1, 256)]
    
    # Escanear cada dirección IP en paralelo
    ips_activas = []
    print(f"{fg('yellow')}\nEscaneando IP's...{attr('reset')}")
    with ThreadPoolExecutor() as executor:
        futuros = [executor.submit(ping, ip) for ip in ips]
        for futuro in as_completed(futuros):
            ip, codigo_retorno = futuro.result()
            if codigo_retorno == 0:
                ips_activas.append(ip)
    
    # Guardar las direcciones IP activas en un archivo pickle
    with open('core/temp/ips.dat', 'wb') as f:
        pickle.dump(ips_activas, f)
    
    # Mostrar la lista de direcciones IP activas
    if ips_activas:
        print(f"{fg('white')}Las siguientes direcciones IP están activas:\n{attr('reset')}")
        for ip in ips_activas:
            print(f"{fg('blue')}{ip}{attr('reset')}")
    else:
        print(f"{fg('red')}No se encontraron direcciones IP activas.{attr('reset')}")

    # Pedir al usuario que elija si desea continuar con el escaneo o escanear otra interfaz de red
    while True:
        eleccion = input(f"{fg('yellow')}\nEnter para continuar con el escaneo, 'Q' para salir, 'R' para re-escanear: {attr('reset')}")
        if eleccion == "":
            # Continuar con el escaneo actual
            subprocess.run(["python", "core/macs.py"])
            subprocess.run(["python", "core/pong2.py"])
            break
        elif eleccion == "R":
            # Escanear otra interfaz de red
            subprocess.run(["python", "core/pong.py"])
            break
        elif eleccion == "Q":
            subprocess.run(["python", "menu.py"])
            break
        else:
            print(f"{fg('red')}Opción inválida.{attr('reset')}")

if __name__ == '__main__':
    # Cargar las variables del archivo variables.dat
    variables = cargar_variables('variables.dat')

    # Extraer las variables necesarias
    interfaz = variables['Interfaz']
    ipv4 = variables['Direccion IPv4']
    gateway = variables['Gateway']

    # Mostrar información de la interfaz, la IPv4 y el gateway
    mostrar_informacion(interfaz, ipv4, gateway)

    # Escanear las direcciones IP en el rango de la red local
    escanear_ips(gateway)
