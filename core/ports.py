import socket
import pickle

def load_ip():
    with open('core/temp/ipselec.dat', 'rb') as file:
        return pickle.load(file)

def scan_port(selected_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.01)  # aumentar el tiempo de espera a 1 segundo
        result = sock.connect_ex((selected_ip, port))
        if result == 0:
            print(f'Puerto {port} abierto')
            return port

def scan_ports(selected_ip):
    print(f'Escaneando puertos abiertos en {selected_ip}...')
    open_ports = []
    for port in range(1, 1025):
        result = scan_port(selected_ip, port)
        if result is not None:
            open_ports.append(result)
    return open_ports

def save_ports(selected_ip, open_ports):
    with open(f'core/temp/{selected_ip}.dat', 'wb') as file:
        pickle.dump(open_ports, file)
    print(f'Puertos guardados en {selected_ip}.dat')

if __name__ == '__main__':
    selected_ip = load_ip()
    open_ports = scan_ports(selected_ip)
    print(f'\n\n{len(open_ports)} puertos abiertos detectados:')
    print(open_ports)
    save_ports(selected_ip, open_ports)
