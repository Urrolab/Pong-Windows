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
    print(f"{fg('magenta')}{interfaz}{attr('reset')}")
    print(f"{fg('green')}IPv4: {fg('blue')}{ipv4}{attr('reset')}")
    print(f"{fg('green')}Gateway: {fg('blue')}{gateway}{attr('reset')}")

def ping(ip):
    """Ejecuta el comando ping para la dirección IP dada y devuelve el código de retorno."""
    proceso_ping = subprocess.run(['ping', '-n', '1', '-w', '500', ip], capture_output=True)
    return ip, proceso_ping.returncode

def escanear_ips(gateway):
    """Realiza un ping a todas las direcciones IP en el rango de la red local
    que se encuentra detrás del gateway proporcionado utilizando hilos."""
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
        print(f"{fg('yellow')}Las siguientes direcciones IP están activas:\n{attr('reset')}")
        for ip in ips_activas:
            print(ip)
    else:
        print(f"{fg('red')}No se encontraron direcciones IP activas.{attr('reset')}")
    input(f"{fg('yellow')}\nPresione Enter para volver al menu principal.{attr('reset')}")

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
