from microbit import *
import gigglebot
threshold = 200
paso = 500
def buscar_luz():
    gigglebot.set_speed(50,50)
    parar = False
    while not parar:
        values = gigglebot.read_sensor(gigglebot.LIGHT_SENSOR, gigglebot.BOTH)
        print(values)
        if values[0] < values[1]:
            gigglebot.turn(gigglebot.LEFT,1000)
        if values[0] > values[1]:
            gigglebot.turn(gigglebot.RIGHT,1000)

        gigglebot.drive(gigglebot.FORWARD, paso)
        suelo = gigglebot.read_sensor(gigglebot.LINE_SENSOR, gigglebot.BOTH)
        if suelo[0] > threshold and suelo [1] > threshold:
            parar = True
        sleep(100)

def main():
    buscar_luz()

if __name__ == "__main__":
    main()