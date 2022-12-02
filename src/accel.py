#!/usr/bin/python3

import time
import board
import adafruit_adxl34x

class Accelerometer():

    _accelerometer = None

    _initialized = False
    _x_offset = .2
    _y_offset = -.3
    _z_offset = -9.0

    def __init__(self):
        try:
            i2c = board.I2C()
            self._accelerometer = adafruit_adxl34x.ADXL343(i2c)
            self._initialized = True
        except ValueError as ve:
            print("Acclerometer not detected")

    def acceleration(self):
        return self._accelerometer.acceleration

    def x(self) -> float:
        if self._accelerometer:
            return self._accelerometer.acceleration[0] + self._x_offset
        else:
            return 0

    def y(self) -> float:
        if self._accelerometer:
            return self._accelerometer.acceleration[1] + self._y_offset
        else:
            return 0

    def z(self) -> float:
        if self._accelerometer:
            return self._accelerometer.acceleration[2] + self._z_offset
        else:
            return 0
    
if __name__ == '__main__':
    accelerometer = Accelerometer()
    while True:
#        a = accelerometer.acceleration()
#        print(f"x: {a[0]}, y: {a[1]}, z: {a[2]}")
        print(f"x: {accelerometer.x()}, y: {accelerometer.y()}, z: {accelerometer.z()}")
        time.sleep(0.2)

