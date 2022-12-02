#!/usr/bin/python3
# initialize the temperature sensor and provide a temperature() method to get the
# current temperature

import logging
import board
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

		self._first = True

	# get the temperature in either Centigrade (units='C') or Fahrenheit (default)
	def temperature(self, units='F'):
		try:
			temp = self.sensor.temperature
		except RuntimeError as e:
			if self._first:
				print(e)
				self._first = False
			temp = 0
		if units == 'C':
			return temp
		else:
			return temp * 9 / 5 + 32

	def __str__(self):
		return self.temperature('F')

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
		logging.info(f"Sensor on GPIO {gpio_pin} initialized")
		return self.sensor


if __name__ == "__main__":
	import time
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("--cht", action="store_true", help="monitor GPIO 5, the CHT")
	parser.add_argument("--egt", action="store_true", help="monitor GPIO 6, the EGT")

	args = parser.parse_args()

	if not args.egt or args.cht:
		args.egt = True
		args.cht = True

	if args.egt:
		print("Monitoring EGT")
		#gpio_pin = board.D6
		ts_egt = TempSensor(board.D6)
	else:
		ts_egt = None
		egt_temp = None

	if args.cht:
		print("Monitoring CHT")
		#gpio_pin = board.D5
		ts_cht = TempSensor(board.D5)
	else:
		ts_cht = None
		cht_temp = ''

	while True:
		if ts_cht:
			cht_temp = ts_cht.temperature()
		if ts_egt:
			egt_temp = ts_egt.temperature()

		out = ""
		if cht_temp > 32 or egt_temp > 32:
			if ts_cht:
				if cht_temp == 32:
					cht_temp = '-'
				out = out + f"CHT temp: {cht_temp}"
			if ts_cht and ts_egt:
				out = out + "\t\t"
			if ts_egt:
				if egt_temp == 32:
					egt_temp = '-'
				out = out + f"EGT temp: {egt_temp}"
			print(out)
		"""		
		if ts.temperature() > 32:
			print(f"It's {ts.temperature()} F degrees.")
		else:
			print(".")
		"""
		time.sleep(1)
