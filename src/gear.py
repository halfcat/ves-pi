#!/usr/bin/python3

import math
import potentiometer
from potentiometer import Potentiometer

# the channel on the ads1015 where the throttle pot is connected 


class Gear(Potentiometer):
	GEAR_CHANNEL = 0

	gear_range = { 
		# 1st is ~19312 / 79%
		'1': { 'min':     19000, 'max':  20000 },
		# N is ~ 20576 / 84%
	 	'N': { 'min':  20000, 'max':  21000 },
		# 2nd is ~ 21648 / 89%
		'2': { 'min':  21300, 'max': 22000 },
		# 3rd is ~ 23072 / 95%
		'3': { 'min': 22700, 'max': 24000 },
		# 4th is 25376 /100%
		'4': { 'min': 25000, 'max': 26000 }
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

