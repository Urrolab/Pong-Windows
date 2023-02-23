import pickle
from scapy.all import *
import mac_vendor_lookup

def obtener_vendor(mac_address):
    try:
        vendor = mac_vendor_lookup.MacLookup().lookup(mac_address)
    except mac_vendor_lookup.VendorNotFoundError:
        vendor = "Desconocido"
    return vendor

def obtener_mac_addresses(ips):
    mac_addresses = {}
    for ip in ips:
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=False)
        if ans:
            mac_address = ans[0][1].hwsrc
            vendor = obtener_vendor(mac_address)
            mac_addresses[ip] = {"mac_address": mac_address, "vendor": vendor}
        else:
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
