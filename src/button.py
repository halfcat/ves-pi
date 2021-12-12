#!/usr/bin/python3

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time


# GPIO 16
pin = 11
c = 0

# button press callback function
def button_down(channel):
	if GPIO.input(pin):
		print("Button is down!")
	else:
		print("Button is up!")

	global c
	c += 1

def button_up(channel):
    print("Button is up!")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Set pin 16 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

GPIO.add_event_detect(pin, GPIO.BOTH, callback=button_down)
#GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_up)

while True:
    print( str(c) + " presses/sec" )
    c = 0
    time.sleep(1)

message = input("Press enter to quit.\n\n")
GPIO.cleanup()


