import radio
from microbit import sleep

def recibir_mensaje():
    tipo, resto, potencia = ["", "", 0.0]
    received = radio.receive_full()
    if received != None:
        mensaje, potencia, _ = received
        mensaje_depurado = str(mensaje[3:], 'utf8')
        tipo, resto = mensaje_depurado[0:2], mensaje_depurado[3:]
    return [tipo, resto, potencia]

def main():
    IDENTIFIER = "00:1"
    SECRETO = "02: navidad"
    PERIOD = 5000
    radio.on()
    gigglebot_ha_llegado = False
    while not gigglebot_ha_llegado:
        radio.config(power = 7, group = 41)
        sleep(PERIOD)
        radio.send(IDENTIFIER)
        print(IDENTIFIER)
        print("pausa")
        mensaje = recibir_mensaje()
        tipo = mensaje[0]
        resto = mensaje[1]
        if tipo == "01" and resto == "dameSecreto":
            gigglebot_ha_llegado = True
    while gigglebot_ha_llegado:
        radio.config(power = 1, group = 41)
        radio.send(SECRETO)
        print(SECRETO)
        sleep(200)

if __name__ == "__main__":
    main()