#!/usr/bin/python3

import time
import board
import adafruit_adxl34x

class Accelerometer():

    _accelerometer = None

    def __init__(self):
        i2c = board.I2C()

        self._accelerometer = adafruit_adxl34x.ADXL343(i2c)

    def acceleration(self):
        return self._accelerometer.acceleration

    def x(self) -> float:
        return self._accelerometer.acceleration[0]

    def y(self) -> float:
        return self._accelerometer.acceleration[1]

    def z(self) -> float:
        return self._accelerometer.acceleration[2]
    
if __name__ == '__main__':
    accelerometer = Accelerometer()
    while True:
#        a = accelerometer.acceleration()
#        print(f"x: {a[0]}, y: {a[1]}, z: {a[2]}")
        print(f"x: {accelerometer.x()}, y: {accelerometer.y()}, z: {accelerometer.z()}")
        time.sleep(0.2)

