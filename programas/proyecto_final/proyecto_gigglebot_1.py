from microbit import *
import gigglebot
import radio
from distance_sensor import DistanceSensor

ds = DistanceSensor()
gigglebot.init()
radio.on()
radio.config(power=1, group=41)
gigglebot.set_speed(50, 50)
paso = 2500

def recibir_mensaje():
    tipo, resto, potencia = ["", "", 0.0]
    received = radio.receive_full()
    if received != None:
        mensaje, potencia, _ = received
        mensaje_depurado = str(mensaje[3:], 'utf8')
        tipo, resto = mensaje_depurado[0:2], mensaje_depurado[3:]
    return [tipo, resto, potencia]

def contar_balizas():
    gigglebot.set_eyes(which=2, R=150, G=150, B=0)
    lista_ids = []
    for n in range(100):
        mensaje = recibir_mensaje()
        tipo = mensaje[0]
        resto = mensaje[1]
        if tipo == "00" and resto not in lista_ids:
            id_baliza = resto
            lista_ids = lista_ids + [id_baliza]
        sleep(100)
    lista_ids.sort()
    return lista_ids

def tomar_medida(id_baliza):
    gigglebot.set_eyes(which=2, R=150, G=0, B=150)
    medidas = []
    suma = 0
    for n in range(200):
        recibir_mensaje()
        mensaje = recibir_mensaje()
        tipo = mensaje[0]
        resto = mensaje[1]
        potencia = mensaje[2]
        if tipo == "00" and resto == id_baliza:
            medidas = medidas + [potencia]
            suma = suma + potencia
        sleep(5)
    if len(medidas) != 0:
        return suma/len(medidas)

def obtener_secreto(id_baliza):
    radio.config(power = 1, group = int(id_baliza))
    gigglebot.set_eyes(which=2, R=0, G=0, B=255)
    secreto_baliza = ""
    while secreto_baliza == "":
        radio.send("01:dameSecreto")
        for n in range(200):
            mensaje = recibir_mensaje()
            tipo = mensaje[0]
            resto = mensaje[1]
            if tipo == "02":
                secreto_baliza = resto
            sleep(5)
    return secreto_baliza

def esquivar_obstaculo(ds):
    distance = ds.read_range_single()
    times = 0
    while distance < 75:
        gigglebot.set_speed(-50, -50)
        gigglebot.turn(gigglebot.LEFT, 1000)
        gigglebot.set_speed(50, 50)
        gigglebot.drive(gigglebot.FORWARD, paso/2)
        gigglebot.turn(gigglebot.LEFT, 1000)
        times = times + 1
        if times > 10:
            gigglebot.set_speed(-50, -50)
            gigglebot.turn(gigglebot.LEFT, 2000)
            gigglebot.set_speed(50, 50)
        distance = ds.read_range_single()
        sleep(50)

def buscar_baliza(id_baliza):
    llegada = False
    radio.config(power = 7, group = 41)
    potencia_anterior = tomar_medida(id_baliza)
    while potencia_anterior == None:
        potencia_anterior = tomar_medida(id_baliza)
    while not llegada:
        gigglebot.drive(gigglebot.FORWARD, paso)
        esquivar_obstaculo(ds)
        potencia_actual = tomar_medida(id_baliza)
        while potencia_actual == None:
            potencia_actual = tomar_medida(id_baliza)
        diferencia_de_potencia = potencia_anterior - potencia_actual
        if diferencia_de_potencia + 2 < 0:
            gigglebot.set_eyes(which=2, R=0, G=0, B=0)
            sleep(200)
            gigglebot.drive(gigglebot.BACKWARD, paso)
            sleep(200)
            gigglebot.set_speed(-50, -50)
            gigglebot.turn(gigglebot.LEFT, 1000)
            gigglebot.set_speed(50, 50)
            sleep(200)
            gigglebot.drive(gigglebot.FORWARD, paso)
            esquivar_obstaculo(ds)
            potencia_actual = tomar_medida(id_baliza)
            while potencia_actual == None:
                potencia_actual = tomar_medida(id_baliza)
            diferencia_de_potencia = potencia_actual - potencia_anterior
            if diferencia_de_potencia + 2 < 0:
                sleep(200)
                gigglebot.drive(gigglebot.BACKWARD, paso)
                sleep(200)
                gigglebot.set_speed(-50, -50)
                gigglebot.turn(gigglebot.RIGHT, 2000)
                gigglebot.set_speed(50, 50)
                sleep(200)
                gigglebot.drive(gigglebot.FORWARD, paso)
                esquivar_obstaculo(ds)
                potencia_actual = tomar_medida(id_baliza)
                while potencia_actual == None:
                    potencia_actual = tomar_medida(id_baliza)
        potencia_anterior = potencia_actual
        if potencia_actual > -70:
            llegada = True

def main():
    baliza = 0
    lista_secretos = {}
    lista_ids = []
    lista_ids = contar_balizas()
    numero_de_balizas = len(lista_ids)
    display.scroll(numero_de_balizas)
    for n in range(numero_de_balizas):
        id_baliza = lista_ids[baliza]
        buscar_baliza(id_baliza)
        secreto_baliza = obtener_secreto(id_baliza)
        lista_secretos[id_baliza] = secreto_baliza
        baliza = baliza + 1
    gigglebot.set_eyes(which=2, R=0, G=0, B=0)

if __name__ == "__main__":
    main()