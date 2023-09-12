from microbit import *
import gigglebot
import radio
from distance_sensor import DistanceSensor

ds = DistanceSensor()
gigglebot.init()
radio.on()
radio.config(power=1, group=41)
gigglebot.set_speed(50, 50)
paso = 2000

def recibir_mensaje():
    tipo, resto, potencia = ["", "", 0.0]
    received = radio.receive_full()
    if received != None:
        mensaje, potencia, _ = received
        mensaje_depurado = str(mensaje[3:], 'utf8')
        tipo, resto = mensaje_depurado[0:2], mensaje_depurado[3:]
    return [tipo, resto, potencia]

def medir_luz():
    medidas = []
    suma = 0
    for n in range(100):
        values = gigglebot.read_sensor(gigglebot.LIGHT_SENSOR, gigglebot.BOTH)
        media = (values[0] + values[1]) / 2
        suma = suma + (media/2)
        sleep(10)
    return suma/100

def esquivar_obstaculo(ds):
    distance = ds.read_range_single()
    times = 0
    while distance < 50:
        gigglebot.set_speed(-50, -50)
        gigglebot.turn(gigglebot.LEFT, 1000)
        gigglebot.set_speed(50, 50)
        gigglebot.drive(gigglebot.FORWARD, paso/2)
        gigglebot.turn(gigglebot.LEFT, 1000)
        times = times + 1
        if times > 20:
            gigglebot.set_speed(-50, -50)
            gigglebot.turn(gigglebot.LEFT, 2000)
            gigglebot.set_speed(50, 50)
        distance = ds.read_range_single()
        sleep(50)

def buscar_meta():
    gigglebot.set_eyes(which=2, R=0, G=0, B=0)
    llegada = False
    luz_anterior = medir_luz()
    contador = 0
    while not llegada:
        gigglebot.drive(gigglebot.FORWARD, paso)
        esquivar_obstaculo(ds)
        luz_actual = medir_luz()
        while luz_actual == 0:
            contador = contador + 1
            gigglebot.turn(gigglebot.LEFT, 1000)
            for n in range(contador):
                if luz_actual == 0:
                    gigglebot.drive(gigglebot.FORWARD, paso)
                    esquivar_obstaculo(ds)
                    luz_actual = medir_luz()
                    sleep(50)
        diferencia_de_luz = luz_actual - luz_anterior
        suelo = gigglebot.read_sensor(gigglebot.LINE_SENSOR, gigglebot.BOTH)
        if suelo[0] < 100 and suelo[1] < 100:
            llegada = True
        elif diferencia_de_luz < 0:
            sleep(200)
            gigglebot.drive(gigglebot.BACKWARD, paso)
            sleep(200)
            gigglebot.set_speed(-50, -50)
            gigglebot.turn(gigglebot.LEFT, 1000)
            gigglebot.set_speed(50, 50)
            sleep(200)
            gigglebot.drive(gigglebot.FORWARD, paso)
            esquivar_obstaculo(ds)
            luz_actual = medir_luz()
            suelo = gigglebot.read_sensor(gigglebot.LINE_SENSOR, gigglebot.BOTH)
            diferencia_de_luz = luz_actual - luz_anterior
            if suelo[0] < 100 and suelo[1] < 100:
                llegada = True
            elif diferencia_de_luz < 0:
                sleep(200)
                gigglebot.drive(gigglebot.BACKWARD, paso)
                sleep(200)
                gigglebot.set_speed(-50, -50)
                gigglebot.turn(gigglebot.RIGHT, 2000)
                gigglebot.set_speed(50, 50)
                sleep(200)
                gigglebot.drive(gigglebot.FORWARD, paso)
                esquivar_obstaculo(ds)
                luz_actual = medir_luz()
        luz_anterior = luz_actual
        suelo = gigglebot.read_sensor(gigglebot.LINE_SENSOR, gigglebot.BOTH)
        if suelo[0] < 100 and suelo[1] < 100:
            llegada = True
        sleep(100)

def comunicar_arbitro(lista_secretos):
    gigglebot.set_eyes(which=2, R=150, G=0, B=150)
    radio.config(power=1, group=43)
    mensaje_arbitro = "03:marcosrp"
    respuesta_arbitro = ""
    for n in lista_secretos:
        mensaje_arbitro = mensaje_arbitro + ",n:lista_secretos[n]"
    while respuesta_arbitro == "":
        radio.send(mensaje_arbitro)
        mensaje = recibir_mensaje()
        tipo = mensaje[0]
        resto = mensaje[1]
        if tipo == "04":
            respuesta_arbitro = resto

def main():
    lista_secretos = {"1":"secreto 1", "2":"secreto 2", "3":"secreto 3"}
    gigglebot.set_eyes(which=2, R=0, G=0, B=0)
    buscar_meta()
    comunicar_arbitro(lista_secretos)
    gigglebot.set_eyes(which=2, R=0, G=0, B=0)

if __name__ == "__main__":
    main()