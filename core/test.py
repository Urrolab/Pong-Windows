import pickle

def cargar_datos_variables():
    with open('temp/ipselec.dat', 'rb') as f:
        return pickle.load(f)

datos = cargar_datos_variables()
print(datos)
