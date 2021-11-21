#!/usr/bin/python3


import potentiometer
from potentiometer import Potentiometer

# the channel on the ads1015 where the throttle pot is connected 

class Throttle(Potentiometer):
	THROTTLE_CHANNEL = 0
	def __init__(self):
		super().__init__(self.THROTTLE_CHANNEL)

if __name__ == '__main__':
	t = Throttle()
	while True:
		print(f"Thottle position: {t.percent()}")
