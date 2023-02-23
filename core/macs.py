import pickle
import mac_vendor_lookup
from scapy.all import *

def obtener_vendor(mac_address):
    """
    Busca el fabricante correspondiente a la dirección MAC dada utilizando la biblioteca mac_vendor_lookup.
    :param mac_address: Una cadena que representa la dirección MAC.
    :return: Una cadena que representa el fabricante correspondiente a la dirección MAC. Si el fabricante no se encuentra,
    se devuelve "Desconocido".
    """
    try:
        vendor = mac_vendor_lookup.MacLookup().lookup(mac_address)
    except mac_vendor_lookup.VendorNotFoundError:
        vendor = "Desconocido"
    return vendor

def obtener_mac_addresses(ips):
    """
    Busca la dirección MAC y el fabricante correspondiente de cada dirección IP utilizando la función srp de Scapy.
    :param ips: Una lista de cadenas que representan las direcciones IP.
    :return: Un diccionario que asigna cada dirección IP a un diccionario que contiene su dirección MAC y fabricante correspondiente.
    """
    mac_addresses = {}
    for i, ip in enumerate(ips):
        print(f"Buscando dirección MAC de {ip} ({i+1}/{len(ips)})...")
        try:
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=False)
            if ans:
                mac_address = ans[0][1].hwsrc
                vendor = obtener_vendor(mac_address)
                mac_addresses[ip] = {"mac_address": mac_address, "vendor": vendor}
            else:
                mac_addresses[ip] = {"mac_address": "No disponible", "vendor": "Desconocido"}
        except:
            mac_addresses[ip] = {"mac_address": "No disponible", "vendor": "Desconocido"}
    return mac_addresses

# Cargar las direcciones IP desde el archivo ips.dat
with open("core/temp/ips.dat", "rb") as f:
    ips = pickle.load(f)

# Obtener la dirección MAC y el fabricante correspondiente de cada dirección IP
mac_addresses = obtener_mac_addresses(ips)

# Guardar la lista de direcciones IP y sus correspondientes direcciones MAC y fabricantes en un archivo pickle
with open("core/temp/macs.dat", "wb") as f:
    pickle.dump(mac_addresses, f)
