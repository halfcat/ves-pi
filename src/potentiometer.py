#!/usr/bin/python3

import board
import busio
import math

import time

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Potentiometer():
	# the min and max raw (voltage) values from the pot
	max_value = 24208
	min_value = 0
	channels = [ ADS.P0, ADS.P1, ADS.P2, ADS.P3 ]

	# initialize the Pot with a channel from 0-3 
	def __init__(self, channel_num=0):
		i2c = busio.I2C(board.SCL, board.SDA)
		ads = ADS.ADS1015(i2c)
		self.channel = self.channels[channel_num]
		self.pot = AnalogIn(ads, self.channel)
	
	# get the reading as a percentage (0 to 100%)
	# TODO:  Implement minv!
	def percent(self, minv=None, maxv=None):
		if minv == None:
			minv = self.min_value
		if maxv == None:
			maxv = self.max_value

		return min(math.trunc((self.value()/maxv)*100), 100)

	# get the raw value
	def value(self):
		return self.pot.value

	def __str__(self):
		return f"{self.value()} / {self.percent()}%"

# kick off a test loop if this file is executed directly
if __name__ == '__main__':
	try:
		pot0 = Potentiometer(0)
	except ValueError as e:
		pot0 = 'n/a'
		print("pot0 not found")

	try:
		pot1 = Potentiometer(1)
	except ValueError as e:
		pot1 = 'n/a'
		print("pot1 not found")

	try:
		pot2 = Potentiometer(2)
	except ValueError as e:
		pot2 = 'n/a'
		print("pot2 not found")

	try:
		pot3 = Potentiometer(3)
	except ValueError as e:
		pot3 = 'n/a'
		print("pot3 not found")


#	pot1 = Potentiometer(1)
#	pot2 = Potentiometer(2)
#	pot3 = Potentiometer(3)

	while True:
		print(f"{pot0} || {pot1} || {pot2} || {pot3}")
		time.sleep(1)
