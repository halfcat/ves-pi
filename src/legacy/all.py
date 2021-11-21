#!/usr/bin/python3

import math
import time
import board
import digitalio

# gpsd packages
import gpsd
#gpsd.connect('/var/run/gpsd.sock')
gpsd.connect()#host='127.0.0.1')



# Temperature sensor
import adafruit_max31855

# A2D for reading pots
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import busio

# Temperature sensor
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
max31855 = adafruit_max31855.MAX31855(spi, cs)


# Set up the a2d board
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)

# define two channels
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)

# get the pot as a percentage
max_value = 24208
def pot_percent(value):
        return min(math.trunc((value/max_value)*100),100)

while True:
    # Get the temperature
    tempC = max31855.temperature
    tempF = tempC * 9 / 5 + 32
    print("Temperature: {} C {} F ".format(tempC, tempF))
    print(f"{chan0.value}/{pot_percent(chan0.value)} || {chan1.value}/{pot_percent(chan1.value)}")
    # GPS data
    packet = gpsd.get_current()
    print( f"lat/long: {packet.position()}")
    print("Speed: {} m/s {} mph ".format(packet.speed(), packet.speed()*2.237))
    #print( f"speed: {packet.speed()} m/s | {

    if False:
            #gpsd.next()
	    print( 'latitude    ' , gpsd.fix.latitude)
	    print( 'longitude   ' , gpsd.fix.longitude)
	    print( 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time)
	    print( 'altitude (m)' , gpsd.fix.altitude)
	    print( 'eps         ' , gpsd.fix.eps)
	    print( 'epx         ' , gpsd.fix.epx)
	    print( 'epv         ' , gpsd.fix.epv)
	    print( 'ept         ' , gpsd.fix.ept)
	    print( 'speed (m/s) ' , gpsd.fix.speed)
	    print( 'climb       ' , gpsd.fix.climb)
	    print( 'track       ' , gpsd.fix.track)
	    print( 'mode        ' , gpsd.fix.mode)
	    print()
	    print('sats        ' , gpsd.satellites)
	    print( "================")
    time.sleep(1)
