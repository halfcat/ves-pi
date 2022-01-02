#!/usr/bin/python3

import neopixel
import board
import time
import threading

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255,255,255)
OFF = (0,0,0)

blue = 0
red = 255

# Valid pins:
# GPIO10, GPIO12, GPIO18 or GPIO21 
# GPIO   Physical Pin
# D10 == 19
# D12 == 32
# D18 == 12
# D21 == 40

pixels = neopixel.NeoPixel(board.D21, 2, auto_write=True, brightness=.2)

pixels[0] = OFF
'''
x = 0
while x < 3:
    pixels[0] = OFF
    time.sleep(.5)
    pixels[0] = RED
    x += 1

time.sleep(1)
pixels[0] = OFF
'''

def get_color(temperature: float, min_temp=100, max_temp=325):
    red = 0
    green = 0
    blue = 0
    
    if temperature < min_temp:
        return (0, 0, 255)
    
    if temperature > max_temp:
        return (255, 0, 0)

    # calculate the position between min and max temp a a value from 0 to 1
    position = (temperature - min_temp) / (max_temp - min_temp)

    ratio = 2 * position
    red = int(max( 0, 255 * (ratio - 1)))
    blue = int(max( 0, 255 * (1 - ratio)))
    green = int(max(0, 255 - blue - red))

    return (red, green, blue)

blinker = True
running = True
def hi_temp_blinker(max_temp=325):
    print("blinker starting")
    while running:
        if temp > max_temp:
            pixels[0] = OFF
            blinker = False
            time.sleep(1)#max( .5, temp-max_temp/)
            blinker = True
        if temp > max_temp+25:
            sleep_time = .25
        else:
            sleep_time = .5
        time.sleep(sleep_time)
    print("blinker stopping")

#blinker_thread = threading.Thread(target=hi_temp_blinker, args=(max_temp,))
#blinker_thread.start()

# max safe operating temp
max_temp = 325
# min warmup temp
min_temp = 100

def set_led(temp):
    if temp > max_temp or temp < min_temp:
        pixels[0] = OFF
        if temp > max_temp+25:
            sleep_time = .15
            pixels.brightness = 1
        else:
            pixels.brightness = .10
            sleep_time = .5
        time.sleep(sleep_time)

#        time.sleep(.5)
    color =  get_color(temp)
    pixels[0] = color


temp = 50
increasing = True
set_led(temp)
time.sleep(2)
while temp < 420 and temp > 40:
    set_led(temp)
    if increasing:
        temp += 10
    else:
        temp -= 10
    if temp >= 375:
        increasing = False
#    print(f"temp: {temp}\tcolor: {color} blink off: {blinker}")
    print(f"temp: {temp}")
    time.sleep(.4)

time.sleep(2)


pixels[0] = OFF

running = False

#pixels[0] = RED
#pixels[8] = BLUE

#pixels.show()

#time.sleep(2)
#pixel = neopixel.NeoPixel(board.D23, 1, pixel_order=neopixel.RGBW)
#pixel[0] = (30, 0, 20, 10)
#pixel.show()
