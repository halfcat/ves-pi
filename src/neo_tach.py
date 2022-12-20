#!/usr/bin/python

import neopixel
import board
import time
from time import sleep
import threading
import sys
import signal
from numpy import clip

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255,255,255)
OFF = (0,0,0)

rpms = 1200
colors = []
blink_on = True

# Valid pins:
# GPIO10, GPIO12, GPIO18 or GPIO21 
# GPIO   Physical Pin
# D10 == 19
# D12 == 32
# D18 == 12
# D21 == 40


def init(max_rpms=10000, max_pixels=8):
    # initialize the array of colors 
    global colors
#    colors = 0 * max_pixels
    tach.brightness = .1

    for x in range(0, max_pixels):
        tach[x] = OFF

        rpms_per_pixel = max_rpms / max_pixels
        if x * rpms_per_pixel <= shift_point:
            colors.append(GREEN)
        elif x * rpms_per_pixel <= red_line:
            colors.append(YELLOW)
        else:
            colors.append(RED)

#        colors.append(OFF)
        
    print(colors)

def rpm_generator(max_rpms=10000):
    rpm_delta = 100
    global rpms
    while True:
        rpms = rpms + rpm_delta
        print(f"RPM's: {rpms:5}")
        sleep(.5)

        if rpms > max_rpms or rpms <= 900:
            rpm_delta *= -1

def tach_runner(tach: neopixel.NeoPixel, shift_point: int, red_line: int):
    '''
    tach_runner() is the thread that manages the set of LED's that should be on all the time
    '''
    global rpms
    global colors
    global blink_on

    while True:
        rpms_per_pixel = max_rpms / max_pixels

        max_x = int(rpms / rpms_per_pixel)
        for x in range(0, max_pixels):
            if max_x < x:
                tach[x] = OFF
    #            print(f"runner turning off x: {x}")
            elif x < max_x: # and blink_on:
                tach[x] = colors[x]
    #            print(f"runner turning ON x: {x}")

        sleep(.1)

def tach_blinker(tach: neopixel.NeoPixel, max_rpms, max_pixels):
    global rpms
    global blink_on
    rpms_per_pixel = max_rpms / max_pixels

    while True:
        blinking_pixel = clip(int(rpms / rpms_per_pixel), 0, max_pixels-1)
#        print(f"{blinking_pixel} = clip(int({rpms} / {rpms_per_pixel}), 0, {max_pixels-1})")
        if blink_on:
            print(f"turning on x: {blinking_pixel}")
            sleep_interval = (rpms % rpms_per_pixel) / rpms_per_pixel

            tach[blinking_pixel] = colors[blinking_pixel]#+(255/sleep_interval,)
        else:
            print(f"turning OFF x: {blinking_pixel}")
            sleep_interval = 1- (rpms % rpms_per_pixel) / rpms_per_pixel
            tach[blinking_pixel] = OFF
            new_x = blinking_pixel

        blink_on = not blink_on
        print(f"sleeping: {sleep_interval}")
        sleep(sleep_interval/2)
    

#graceful-ish shutdown
def signal_handler(sig, frame):
    print('Exiting...')
    for x in range(0, max_pixels):
        tach[x] = OFF
    sys.exit(0)


if __name__ == '__main__':
    max_pixels = 8


    max_rpms = 10000
    max_generated_rpms = 10200
    shift_point = 6000
    red_line = 7500
    rpms = 2000
    blink_on = False

    tach = neopixel.NeoPixel(board.D21, max_pixels, auto_write=True, brightness=.2)
    signal.signal(signal.SIGINT, signal_handler)

    init()

    tach_thread = threading.Thread(target=tach_runner, args=(tach, shift_point,red_line))
    tach_thread.start()
    sleep(0.5)

    tach_blinker_thread = threading.Thread(target=tach_blinker, args=(tach, max_rpms, max_pixels,))
    tach_blinker_thread.start()

    rpm_generator_thread = threading.Thread(target=rpm_generator, args=(max_generated_rpms,))
    rpm_generator_thread.start()
