import pyfiglet, os
from colored import fg, attr

# Imprime el título en ASCII art
titulo = pyfiglet.figlet_format("PONG")
print(titulo)

def eliminar_archivos_temp():
    # Especificamos la ruta del directorio
    ruta = "core/temp"
    
    # Obtenemos una lista de todos los archivos en el directorio
    archivos = os.listdir(ruta)
    
    # Eliminamos cada archivo en la lista
    for archivo in archivos:
        # Combinamos la ruta con el nombre del archivo
        ruta_archivo = os.path.join(ruta, archivo)
        
        # Verificamos que el archivo sea un archivo y no un directorio
        if os.path.isfile(ruta_archivo):
            # Eliminamos el archivo
            os.remove(ruta_archivo)

# Define las funciones para ejecutar cada opción
def ejecutar_pong():
    os.system("python core/pong.py")

def ejecutar_contacto():
    os.system("cls")
    contacto = pyfiglet.figlet_format("UwU")
    print(contacto)
    print(f"{fg('magenta')}Autor: {fg('white')}Uriel Dobrovolsky{attr('reset')}")
    print(f"{fg('green')}Email: {fg('white')}urieldobrovolsky1996@gmail.com{attr('reset')}")
    print(f"{fg('blue')}LinkedIn: {fg('white')}https://www.linkedin.com/in/urro/{attr('reset')}")
    input("\nEnter para continuar...")

# Define un diccionario que mapea opciones con funciones
opciones = {
    "1": ejecutar_pong,
    "2": ejecutar_contacto,
    "3": exit,
}

# Define una función para mostrar el menú y obtener la selección del usuario
def mostrar_menu():
    print(f"{fg('green')}1.{attr('reset')} Ejecutar análisis")
    print(f"{fg('green')}2.{attr('reset')} Contacto")
    print(f"{fg('red')}{attr('bold')}\n3.{attr('reset')} Salir")

# Define una función para manejar la entrada del usuario y validar las opciones
def manejar_opcion(opcion):
    if opcion in opciones:
        opciones[opcion]()
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")

# Muestra el menú y maneja la entrada del usuario hasta que el usuario elige salir
while True:
    os.system("cls")
    print(f"{titulo}Windows version\n=------------------------=\n")
    eliminar_archivos_temp()
    mostrar_menu()
    opcion = input(f"{fg('yellow')}Seleccione una opción: {attr('reset')}")
    manejar_opcion(opcion)
