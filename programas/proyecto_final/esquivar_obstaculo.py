from microbit import *
import gigglebot
from distance_sensor import DistanceSensor
paso = 500

def esquivar_obstaculo(ds):
    distance = ds.read_range_single()
    while distance < 100:
        gigglebot.set_speed(-50,-50)
        gigglebot.turn(gigglebot.LEFT,1000)
        gigglebot.set_speed(50,50)
        gigglebot.drive(gigglebot.FORWARD, paso)
        gigglebot.turn(gigglebot.LEFT,1000)
        distance = ds.read_range_single()
        sleep(50)

def main():
    ds = DistanceSensor()
    while True:
        gigglebot.drive(gigglebot.FORWARD, paso)
        esquivar_obstaculo(ds)
        sleep(50)


if __name__ == "__main__":
    main()