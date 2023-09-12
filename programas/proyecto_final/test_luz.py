from microbit import *
import gigglebot
import radio

def medir_luz():
    medidas = []
    suma = 0
    for n in range(10):
        values = gigglebot.read_sensor(gigglebot.LIGHT_SENSOR, gigglebot.BOTH)
        media = (values[0] + values[1]) / 2
        suma = suma + (media/2)
        sleep(10)
    return suma/10

def main():
    while True:
        luz = medir_luz()
        print(luz)
        sleep(500)

if __name__ == "__main__":
    main()