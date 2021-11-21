#!/usr/bin/python3

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

class Tach:
	# GPIO 16 is pin #36 when using physical board pin numbers
	#tach_pin = 36
	# 16 is the Broadcom numbering scheme
	tach_pin = 16
	c = 0

	GPIO = None
	# The window of time that we're monitoring to calculate RPM's
	# in SECONDS
	time_slice = .5
	last_time = 0

	last_time = time.time()
	this_time = time.time()
	rpm = 0
	max_allowed_rpms = 15000
	max_rpms = 0

	def spark_detected(self, channel):
		"""spark detection callback function"""
		self.this_time = time.time()
		rpm = (1/(self.this_time - self.last_time)) * 60
		if rpm <= self.max_allowed_rpms:
			self.rpm = rpm
		else:
			print(f"discarded OOB value {rpm:.0f}")
		self.last_time = self.this_time	
		if self.rpm > self.max_rpms:
			self.max_rpms = self.rpm

	def __init__(self):
		"""Set up the GPIO pin and register a callback function for spark detection"""
		GPIO.setwarnings(False) # Ignore warning for now
		print(f"Using {GPIO.getmode()} mode for pin numbering")
		GPIO.setmode(GPIO.BCM) # Use physical pin numbering
		print(f"Mode set.  Using {GPIO.getmode()} mode for pin numbering")

		# Set pin 16 to be an input pin and set initial value to be pulled low (off)
		GPIO.setup(self.tach_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
		GPIO.add_event_detect(self.tach_pin, GPIO.RISING, callback=self.spark_detected)

	def rpms(self) -> int:
		"""Return the current RPM's based on the last second
		If the RPM's drop below 60 RPM's (less than one spark/second,
		assume the motor stopped and reset motor to zero
		"""
		if time.time() - self.last_time > 1:
			self.rpm = 0
		return self.rpm
			

if __name__ == '__main__':
	tach = Tach()
try:
	while True:
		rpms = tach.rpms()
		if rpms > 0:
			print(f"{rpms:.0f} RPM's")
		time.sleep(1)
except:
	print( "Shutting down")
	time.sleep(2)
	GPIO.remove_event_detect(tach.tach_pin)
	GPIO.cleanup()
	print(f"Max RPM's: {tach.max_rpms:.0f}")
