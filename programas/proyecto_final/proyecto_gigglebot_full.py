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
    for n in range(100):
        recibir_mensaje()
        mensaje = recibir_mensaje()
        tipo = mensaje[0]
        resto = mensaje[1]
        potencia = mensaje[2]
        if tipo == "00" and resto == id_baliza:
            medidas = medidas + [potencia]
            suma = suma + potencia
        sleep(10)
    if len(medidas) != 0:
        return suma/len(medidas)

def obtener_secreto():
    radio.config(power=1, group=41)
    gigglebot.set_eyes(which=2, R=0, G=0, B=255)
    secreto_baliza = ""
    while secreto_baliza == "":
        radio.send("01:dameSecreto")
        for n in range(100):
            mensaje = recibir_mensaje()
            tipo = mensaje[0]
            resto = mensaje[1]
            if tipo == "02":
                secreto_baliza = resto
            sleep(10)
    return secreto_baliza

def esquivar_obstaculo(ds):
    distance = ds.read_range_single()
    times = 0
    while distance < 75:
        gigglebot.set_speed(-50, -50)
        gigglebot.turn(gigglebot.LEFT, 800)
        gigglebot.set_speed(50, 50)
        gigglebot.drive(gigglebot.FORWARD, paso/2)
        gigglebot.turn(gigglebot.LEFT, 800)
        times = times + 1
        if times > 20:
            gigglebot.set_speed(-50, -50)
            gigglebot.turn(gigglebot.LEFT, 2000)
            gigglebot.set_speed(50, 50)
        distance = ds.read_range_single()
        sleep(50)

def buscar_baliza(id_baliza):
    llegada = False
    potencia_anterior = tomar_medida(id_baliza)
    while potencia_anterior == None:
        potencia_anterior = tomar_medida(id_baliza)
    while not llegada:
        gigglebot.set_eyes(which=2, R=0, G=255, B=0)
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
            gigglebot.turn(gigglebot.LEFT, 800)
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
                gigglebot.turn(gigglebot.RIGHT, 1600)
                gigglebot.set_speed(50, 50)
                sleep(200)
                gigglebot.drive(gigglebot.FORWARD, paso)
                esquivar_obstaculo(ds)
                potencia_actual = tomar_medida(id_baliza)
                while potencia_actual == None:
                    potencia_actual = tomar_medida(id_baliza)
        potencia_anterior = potencia_actual
        if potencia_actual > -60:
            llegada = True

def medir_luz():
    medidas = []
    suma = 0
    for n in range(100):
        values = gigglebot.read_sensor(gigglebot.LIGHT_SENSOR, gigglebot.BOTH)
        media = (values[0] + values[1]) / 2
        suma = suma + (media/2)
        sleep(10)
    return suma/100

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
            gigglebot.turn(gigglebot.LEFT, 800)
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
            gigglebot.turn(gigglebot.LEFT, 800)
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
                gigglebot.turn(gigglebot.RIGHT, 1600)
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
    baliza = 0
    lista_secretos = {}
    lista_ids = []

    lista_ids = contar_balizas()
    numero_de_balizas = len(lista_ids)
    display.scroll(numero_de_balizas)
    for n in range(numero_de_balizas):
        id_baliza = lista_ids[baliza]
        buscar_baliza(id_baliza)
        secreto_baliza = obtener_secreto()
        lista_secretos[id_baliza] = secreto_baliza
        baliza = baliza + 1
    buscar_meta()
    comunicar_arbitro(lista_secretos)
    strip[2]=(248, 12, 18)
    strip[3]=(255, 68, 34)
    strip[4]=(255, 153, 51)
    strip[5]=(208, 195, 16)
    strip[6]=(34, 204, 170)
    strip[7]=(51, 17, 187)
    strip[8]=(68, 34, 153)
    strip.show()


if __name__ == "__main__":
    main()