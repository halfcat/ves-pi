from temp_sensor import TempSensor
import board

class Cht(TempSensor):
	"""Create an object which can be used to read the Cht
	"""

	# the pin used for the CHT
	cht_pin = board.D5

	def __init__(self, force_reinit=False):
		if self.sensor == None or force_reinit == True:
			self.init_sensor(self.cht_pin)



if __name__ == "__main__":
    import time
    cht = Cht()
    while True:
        print(f"It's {cht.temperature()} F degrees.")
        time.sleep(1)

