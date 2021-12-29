#!/usr/bin/python3

import math

import potentiometer
from potentiometer import Potentiometer

# the channel on the ads1015 where the throttle pot is connected 

class Throttle(Potentiometer):
	THROTTLE_CHANNEL = 1
	_raw_max_throttle = 11200
	_raw_min_throttle = 128

	def __init__(self):
		super().__init__(self.THROTTLE_CHANNEL)

	def percent(self):
		return math.trunc(max(self.value() - self._raw_min_throttle, 0) / self._raw_max_throttle * 100)
#		return (min( math.trunc( max(self.value() - self._raw_min_throttle, 0) / self._raw_max_throttle			)*100), 100)

if __name__ == '__main__':
	t = Throttle()
	while True:
		print(f"Thottle position: {t.percent()}")
		#print(f"Thottle position: {t.percent()} ({t.value()}")
