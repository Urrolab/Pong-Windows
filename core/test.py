import pickle

def cargar_datos_variables():
    with open('core/temp/macs.dat', 'rb') as f:
        return pickle.load(f)

datos = cargar_datos_variables()
print(datos)
