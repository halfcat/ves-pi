#!/usr/bin/python3

import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import math

import time

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1015(i2c)

chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)

max_value = 24208

def pot_percent(value):
	return min(math.trunc((value/max_value)*100),100)

while True:
	print(f"{chan0.value}/{pot_percent(chan0.value)} || {chan1.value}/{pot_percent(chan1.value)} || {chan2.value}/{pot_percent(chan2.value)}")
	time.sleep(1)
