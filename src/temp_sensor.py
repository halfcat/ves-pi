# initialize the temperature sensor and provide a temperature() method to get the
# current temperature

import board
import digitalio
import adafruit_max31855
from digitalio import DigitalInOut

class TempSensor:
	sensor = None
	gpio_pin = board.D5

	def __init__(self, force_reinit=False):
		if self.sensor == None or force_reinit == True:
			self.sensor = self.init_sensor(self.gpio_pin)

	# get the temperature in either Centigrade (units='C') or Fahrenheit (default)
	def temperature(self, units='F'):
		temp = self.sensor.temperature
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
		spi = board.SPI()
		self.gpio_pin = gpio_pin
		cs = DigitalInOut(self.gpio_pin)
		self.sensor = adafruit_max31855.MAX31855(spi, cs)
		return self.sensor


if __name__ == "__main__":
	import time
	ts = TempSensor()
	while True:
		print(f"It's {ts.temperature()} F degrees.")
		time.sleep(1)
