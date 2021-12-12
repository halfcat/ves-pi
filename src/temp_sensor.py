#!/usr/bin/python3
# initialize the temperature sensor and provide a temperature() method to get the
# current temperature

import board
#import digitalio
import adafruit_max31855
from digitalio import DigitalInOut


class TempSensor:
	sensor = None
	# GPIO 5 is EGT (no probe at the moment)
	# GPIO 6 is CHT (has probe)

	## GPIO5 / D5 is the CS signal
	#_gpio_pin = board.D5
	_gpio_pin = board.D6

	def __init__(self, gpio_pin, force_reinit=False):
		if self.sensor == None or force_reinit == True:
			self.sensor = self.init_sensor(gpio_pin)

	# get the temperature in either Centigrade (units='C') or Fahrenheit (default)
	def temperature(self, units='F'):
		try:
			temp = self.sensor.temperature
		except RuntimeError as e:
			print(e)
			temp = 0
		if units == 'C':
			return temp
		else:
			return temp * 9 / 5 + 32

	def __str__(self):
		return sensor.temperature('F')

	# initialize the sensor
	def init_sensor(self, gpio_pin): # -> adafruit_max31855:
		""" Initialize the temperature sensor
		connect up the sensor and connect it to the GPIO pin
		"""
		print(f"Initializing Sensor on GPIO {gpio_pin}")
		spi = board.SPI()
		self._gpio_pin = gpio_pin
		# Chip select
		cs = DigitalInOut(self._gpio_pin)
		self.sensor = adafruit_max31855.MAX31855(spi, cs)
		return self.sensor


if __name__ == "__main__":
	import time
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("--cht", action="store_true", help="monitor GPIO 5, the CHT")
	parser.add_argument("--egt", action="store_true", help="monitor GPIO 6, the EGT")

	args = parser.parse_args()

	if args.egt:
		gpio_pin = board.D6
	else:
		gpio_pin = board.D5

	ts = TempSensor(gpio_pin)
	print(f"Using GPIO {ts._gpio_pin}")
	while True:
		if ts.temperature() > 32:
			print(f"It's {ts.temperature()} F degrees.")
		else:
			print(".")
		time.sleep(1)
