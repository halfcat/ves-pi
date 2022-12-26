# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for RGB character LCD on Raspberry Pi"""
import time
import board
import digitalio
import pwmio
import adafruit_character_lcd.character_lcd as characterlcd

import threading
import sys
import signal

# Modify this if you have a different sized character LCD
lcd_columns = 20
lcd_rows = 4

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)  # LCD pin 4
lcd_en = digitalio.DigitalInOut(board.D19)  # LCD pin 6
lcd_d7 = digitalio.DigitalInOut(board.D27)  # LCD pin 14
lcd_d6 = digitalio.DigitalInOut(board.D22)  # LCD pin 13
lcd_d5 = digitalio.DigitalInOut(board.D24)  # LCD pin 12
lcd_d4 = digitalio.DigitalInOut(board.D25)  # LCD pin 11

# LCD pin 5.  Determines whether to read to or write from the display.
#lcd_rw = digitalio.DigitalInOut( board.D4)  
# Not necessary if only writing to the display. Used on shield.

red = pwmio.PWMOut(board.D21)
green = pwmio.PWMOut(board.D12)
blue = pwmio.PWMOut(board.D18)

# Initialize the LCD class
# The lcd_rw parameter is optional.  You can omit the line below if you're only
# writing to the display.
lcd = characterlcd.Character_LCD_RGB(
    lcd_rs,
    lcd_en,
    lcd_d4,
    lcd_d5,
    lcd_d6,
    lcd_d7,
    lcd_columns,
    lcd_rows,
    red,
    green,
    blue,
)

RED   = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE  = [0, 0, 100]
OFF   = [0, 0, 0]


def get_color(temperature: float, min_temp=100, max_temp=325)->list:
    '''Get a list with an RGB set in it for gradating from min_tmp to max_temp'''
    red = 0
    green = 0
    blue = 0

    # the max color value
    max_color = 100
    
    if temperature < min_temp:
        return (0, 0, max_color)
    
    if temperature > max_temp:
        return (max_color, 0, 0)

    # calculate the position between min and max temp a a value from 0 to 1
    position = (temperature - min_temp) / (max_temp - min_temp)

    ratio = 2 * position
    red = int(max( 0, max_color * (ratio - 1)))
    blue = int(max( 0, max_color * (1 - ratio)))
    green = int(max(0, max_color - blue - red))

    return [red, green, blue]

global temp
temp = 250

def temp_generator(max_temp=350, min_temp=60, temp_delta=10):
    '''Dummy temperatue generator'''
    global temp
    while True:
        temp = temp + temp_delta
        print(f"temp: {temp:5}")
        time.sleep(.5)

        if temp > max_temp or temp <= min_temp:
            temp_delta *= -1


#rpm_generator_thread = threading.Thread(target=temp_generator, args=(350,60))
#rpm_generator_thread.start()

#graceful-ish shutdown
def signal_handler(sig, frame):
    print('Exiting...')
    lcd.clear()
    lcd.message = "Goodbye!"
    time.sleep(1)
    lcd.clear()
    lcd.color = OFF
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

lcd.clear()
lcd.color = OFF
# Set LCD color to red
#lcd.color = [100, 100, 100]
# wake & blink
lcd.color = RED  #|---+----|----+----|
lcd.message =  "\n The Ves-Pi Project" 
time.sleep(1)

# blink three times
lcd.color = OFF
time.sleep(.25)
lcd.color = RED
time.sleep(.25)
lcd.color = OFF
time.sleep(.25)
lcd.color = RED
time.sleep(.25)
lcd.clear()

# initialize and start the temp generator thread
temp = 80
temp_generator_thread = threading.Thread(target=temp_generator, args=(400,60,10,))
temp_generator_thread.start()

rpms = 8200

lcd.message =   f"RPMs {rpms:5}  MPH:   0\nThrot:  0%  Gear:  N\nCHT:   {temp:3}  EGT:  77\nx:-0.4 y:-1.1 z:-0.0"


blink = True
last_color = [0,0,0]
while True:
#                |---+----|----+----| |---+----|----+----|  |---+----|----+----|  |---+----|----+----|
    lcd.message =   f"RPMs {rpms:5}  MPH:   0\nThrot:  0%  Gear:  N\nCHT:   {temp:3}  EGT:  77\nx:-0.4 y:-1.1 z:-0.0"
    #lcd.cursor_position(7, 2)
    #lcd.message=f"{temp:3}"

    lcd.color = get_color(temp)
#    if temp >= 350 and blink:
#        lcd.color = OFF
#    else:
#        lcd.color = get_color(temp)
    color = get_color(temp)
    if color != last_color:
        lcd.color = color
        print(color)
    last_color = color
#    blink = not blink

    time.sleep(.25)


def temp_generator(max_temp=375, min_temp=60):
    temp_delta = 5
    global temp
    while True:
        temp = temp + temp_delta
        print(f"temp: {temp:5}")
        sleep(.5)

        if temp > max_temp or temp <= min_temp:
            temp_delta *= -1
