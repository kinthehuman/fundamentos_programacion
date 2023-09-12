from microbit import *
import gigglebot
import radio
radio.on
radio.config(power=0, group=41)
id_baliza = "1"
def tomar_medida():

    medidas = []
    suma = 0
    for n in range(100):

        received = radio.receive_full()
        if received != None:
            mensaje, potencia, _ = received
            mensaje_depurado = str(mensaje[3:], 'utf8')
            tipo, resto= mensaje_depurado[0:2],mensaje_depurado[3:]

            if tipo == "00" and resto == id_baliza:
                medidas = medidas + [potencia]
                suma = suma + potencia

        sleep(100)

    if len(medidas) != 0:
        return suma/len(medidas)

def obtener_secreto():
    #radio.send("01:dameSecreto")
    #sleep(1000)
    for n in range(10):
        received = radio.receive_full()
        if received != None:
            mensaje, potencia, _ = received
            mensaje_depurado = str(mensaje[3:], 'utf8')
            tipo, resto= mensaje_depurado[0:2],mensaje_depurado[3:]
            if tipo == "02":
                secreto_baliza = resto
        sleep(200)



def buscar_baliza():
    gigglebot.set_speed(50,50)
    paso = 2000
    radio.on()
    llegada = False
    potencia_anterior = tomar_medida()
    secreto_baliza = ""

    while not llegada:

        gigglebot.drive(gigglebot.FORWARD, paso)
        obtener_secreto()
        potencia_actual = tomar_medida()
        diferencia_de_potencia = potencia_actual - potencia_anterior
        print(diferencia_de_potencia)
        if diferencia_de_potencia < 0:
            sleep(200)
            gigglebot.drive(gigglebot.BACKWARD, paso)
            sleep(200)
            gigglebot.set_speed(-50,-50)
            gigglebot.turn(gigglebot.LEFT,1000)
            gigglebot.set_speed(50,50)
            sleep(200)
            gigglebot.drive(gigglebot.FORWARD, paso)
            obtener_secreto()
            potencia_actual = tomar_medida()
            diferencia_de_potencia = potencia_actual - potencia_anterior
            print(diferencia_de_potencia)

            if diferencia_de_potencia < 0:
                sleep(200)
                gigglebot.drive(gigglebot.BACKWARD, paso)
                sleep(200)
                gigglebot.set_speed(-50,-50)
                gigglebot.turn(gigglebot.RIGHT,2000)
                gigglebot.set_speed(50,50)
                sleep(200)
                gigglebot.drive(gigglebot.FORWARD, paso)
                obtener_secreto()
                potencia_actual = tomar_medida()


        potencia_anterior = potencia_actual
        if secreto_baliza != "":
            llegada = True
        sleep(500)

def main():
    buscar_baliza()

if __name__ == "__main__":
    main()