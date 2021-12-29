#!/usr/bin/python3

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

class Tach:
	debug = False

	# GPIO 16 is pin #36 when using physical board pin numbers
	#tach_pin = 
	# 12 is the Broadcom numbering scheme
	tach_pin = 12
	c = 0

	GPIO = None

	last_time = time.time_ns()
	this_time = time.time_ns()
	rpm = 0
	_max_allowed_rpms = 9000
	# Avoid false sparks where the signal hovers at a threshold
	_bounce_delay = 0
	max_rpms = 0


	def spark_detected(self, channel):
		"""
		spark detection callback function
		"""
		# edge debounce

    	# only deal with valid edges
		if True:
			self.this_time = time.time_ns()
		#	print(f"elapsed ns:  {self.this_time - self.last_time}")
			rpm = (1/(self.this_time - self.last_time)) * 60*1000000000
			self.last_time = self.this_time	
			if rpm <= self._max_allowed_rpms:
				self.rpm = rpm
			elif self.debug:
				print(f"discarded OOB value {rpm:.0f}")

	def __init__(self):
		"""Set up the GPIO pin and register a callback function for spark detection"""
#		GPIO.setwarnings(False) # Ignore warning for now
#		print(f"Using {GPIO.getmode()} mode for pin numbering")
		GPIO.setmode(GPIO.BCM) # Use physical pin numbering
#		print(f"Mode set.  Using {GPIO.getmode()} mode for pin numbering")
		rps = self._max_allowed_rpms / 60
		self._bounce_delay = 1 / rps
		bouncetime = int(self._bounce_delay*1000)

		# Set pin 16 to be an input pin and set initial value to be pulled low (off)
		#GPIO.setup(self.tach_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
		GPIO.setup(self.tach_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
		# bouncetime param is milliSec, but _bounce_delay is seconds
		#GPIO.add_event_detect(self.tach_pin, GPIO.RISING, callback=self.spark_detected, bouncetime=bouncetime)
		GPIO.add_event_detect(self.tach_pin, GPIO.FALLING, callback=self.spark_detected, bouncetime=bouncetime)

	def rpms(self) -> int:
		"""Return the current RPM's based on the last second
		If the RPM's drop below 60 RPM's (less than one spark/second,
		assume the motor stopped and reset motor to zero
		"""
		if time.time_ns() - self.last_time > 1:
			self.rpm = 0
		return self.rpm
			

if __name__ == '__main__':
	tach = Tach()
	try:
		while True:
			rpms = tach.rpms()
			if rpms > 0:
				#print(f"{rpms:.0f} RPM's")
				x2 = rpms / 2
				print(f"{rpms:.0f} RPM's")
			time.sleep(.5)
	except:
		print( "Shutting down")
		time.sleep(1)
		GPIO.remove_event_detect(tach.tach_pin)
		GPIO.cleanup()
		print(f"Max RPM's: {tach.max_rpms:.0f}")
