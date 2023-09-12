from microbit import *
import gigglebot
from distance_sensor import DistanceSensor
def main():
    ds = DistanceSensor()
    while True:
        if button_a.was_pressed():
            distance = ds.read_range_single()
            display.scroll(distance)

if __name__ == "__main__":
    main()