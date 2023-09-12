from microbit import *
import radio

radio.on()
radio.config(power=1, group=43)

def recibir_mensaje():
    tipo, resto, potencia = ["", "", 0.0]
    received = radio.receive_full()
    if received != None:
        mensaje, potencia, _ = received
        mensaje_depurado = str(mensaje[3:], 'utf8')
        tipo, resto = mensaje_depurado[0:2], mensaje_depurado[3:]
    return [tipo, resto, potencia]

def main():
    while True:
        mensaje = recibir_mensaje()
        tipo = mensaje[0]
        resto = mensaje[1]
        if tipo == "03":
            radio.send("04:recibido")
            print("recibido")
        sleep(200)

if __name__ == "__main__":
    main()