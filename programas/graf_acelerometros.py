from microbit import *

def generar_tupla():
    x = float(accelerometer.get_x())
    y = float(accelerometer.get_y())
    z = float(accelerometer.get_z())
    #x = random.randrange(1,10)
    #y = random.randrange(1,10)
    #z = random.randrange(1,10)
    t = (x,y,z)
    return t

def insertar_tupla(lista,MAX,tupla):
    if len(lista) < MAX:
        lista.append(tupla)
    else:
        lista = lista[1:]
        lista.append(tupla)

    return lista

def calcular_medias(lista):
    l = len(lista)
    x = 0.0
    y = 0.0
    z = 0.0
    for n in range(l):
        t = lista[n]
        x = x + t[0]
        y = y + t[1]
        z = z + t[2]
    xm = x/l
    ym = y/l
    zm = z/l
    medias = (xm,ym,zm)
    return medias

lista_de_valores = []
while True:
    tupla = generar_tupla
    lista_de_valores = insertar_tupla(lista_de_valores,10,tupla)
    medias = calcular_medias(lista_de_valores)
    print(medias)





