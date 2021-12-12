#!/usr/bin/python3

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import logging


class Clutch():
	"""The clutch is measured as a button that's closed when the clutch is out"""
	# BCM GPIO 17 / Physical pin 11
	pin = 17
	in_gear = False
	# button press callback function
	def _button_down(self,channel):
		if GPIO.input(self.pin):
			# Button is down
			self.in_gear = True
			logging.debug("Motor in gear")
		else:
			# Button is up
			self.in_gear = False
			logging.debug("Motor out of gear")

	def __init__(self, gpio_pin=None):
		GPIO.setwarnings(False) # Ignore warning for now
		#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

		# Set pin to be an input pin and set initial value to be pulled low (off)
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
		GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self._button_down)

if __name__ == "__main__":
	clutch = Clutch()
	while True:
		if clutch.in_gear:
			print("Motor in gear")
		else:
			print("Motor is OUT of gear")
		time.sleep(1)

	message = input("Press enter to quit.\n\n")
	GPIO.cleanup()


