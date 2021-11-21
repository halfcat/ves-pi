#!/usr/bin/python3

import math
import potentiometer
from potentiometer import Potentiometer

# the channel on the ads1015 where the throttle pot is connected 


class Gear(Potentiometer):
	GEAR_CHANNEL = 1

	gear_range = { 
		'N': { 'min':  4000, 'max':  7000 },
		1: { 'min':     0, 'max':  3000 },
		2: { 'min':  8000, 'max': 11000 },
		3: { 'min': 12000, 'max': 15000 },
		4: { 'min': 16000, 'max': 19000 }
	}
	def __init__(self):
		super().__init__(self.GEAR_CHANNEL)

	# The gear is returned as 0-4, where 0 represents Neutral
	# and 1-4 are first through 4th
	def gear(self) -> chr:
		v = super().value()
		for g in self.gear_range:
			min = self.gear_range[g]['min']
			max = self.gear_range[g]['max']
			#print(f"gear:  {g}, min:  {min}, max:  {max}")
			if v >= min and v <= max:
				return g

if __name__ == '__main__':
	import time
	g = Gear()

	while True:
		print(f"Current gear: {g.gear()}")
		time.sleep(1)

