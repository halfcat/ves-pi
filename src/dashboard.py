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


class Dashboard():
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

    RED   = [100, 0, 0]
    GREEN = [0, 100, 0]
    BLUE  = [0, 0, 100]
    OFF   = [0, 0, 0]

    _lcd = None
    _status = {}
    _status['rpms'] = 1200
    _status['mph'] = 85
    _status['throttle'] = 100
    _status['gear'] = '4'
    _status['egt_temp'] = 1600
    _status['temp'] = 80


    def __init__(self):
        # Initialize the LCD class
        # The lcd_rw parameter is optional.  You can omit the line below if you're only
        # writing to the display.
        self._lcd = characterlcd.Character_LCD_RGB(
            self.lcd_rs,
            self.lcd_en,
            self.lcd_d4,
            self.lcd_d5,
            self.lcd_d6,
            self.lcd_d7,
            self.lcd_columns,
            self.lcd_rows,
            self.red,
            self.green,
            self.blue,
        )
        signal.signal(signal.SIGINT, self.signal_handler)

        self.self_test(self._lcd)


    def update(self, status:dict):
        self._status = status

    def start_display(self, update_frequency=0.25):
        display_updater_thread = threading.Thread(target=self.display_updater, args=(self._lcd, update_frequency,))
        display_updater_thread.start()

    def display_updater(self, lcd, update_frequency=0.25):
        blink = True
        last_color = [0,0,0]

        while True:
            rpms = self._status.get('rpms')
            mph = self._status.get('mph')
            throttle = self._status.get('throttle')
            gear = self._status.get('gear')
            egt_temp = self._status.get('egt_temp')
            temp = self._status.get('temp')
        
        #                     |---+----|----+----| |---+----|----+----|  |---+----|----+----|  |---+----|----+----|
            lcd.message =   f"RPMs {rpms:5}  MPH: {mph:3}\nThrot:{throttle:3}%  Gear:  {gear}\nCHT:   {temp:3}  EGT:{egt_temp:4}\nx:-0.4 y:-1.1 z:-0.0"
            if temp >= 350 and blink:
                lcd.color = self.OFF
            else:
                lcd.color = self._get_color(temp)
            blink = not blink

            time.sleep(update_frequency)

    def self_test(self, lcd):
        lcd.clear()
        lcd.color = self.OFF
        # Set LCD color to red
        #lcd.color = [100, 100, 100]
        # wake & blink
        lcd.color = self.RED  #|---+----|----+----|
        lcd.message =  "\n The Ves-Pi Project" 
        time.sleep(1)

        # blink three times
        lcd.color = self.OFF
        time.sleep(.25)
        lcd.color = self.RED
        time.sleep(.25)
        lcd.color = self.OFF
        time.sleep(.25)
        lcd.color = self.RED
        time.sleep(.25)
        lcd.clear()


    def _get_color(self, temperature: float, min_temp=100, max_temp=325)->list:
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

    #graceful-ish shutdown
    def signal_handler(self, sig, frame):
        print('Exiting...')
        time.sleep(1)
        self._lcd.clear()
        self._lcd.message = "Goodbye!"
        time.sleep(1)
        self._lcd.clear()
        self._lcd.color = self.OFF

##################################
def temp_generator(d, max_temp=350, min_temp=60, temp_delta=10):
    '''Dummy temperatue generator'''
    #global temp
    status = {}
    status['rpms'] = 1200
    status['mph'] = 85
    status['throttle'] = 100
    status['gear'] = 4
    status['egt_temp'] = 1200
    status['temp'] = min_temp

    while True:
        status['temp'] += temp_delta
        print(f"temp: {status['temp']:5}")
        d.update(status)
        time.sleep(.5)

        if status['temp'] > max_temp or status['temp'] <= min_temp:
            temp_delta *= -1


if __name__ == '__main__':
    d = Dashboard()
    d.start_display(0.5)
    #d.update(status_dict)

    # initialize and start the temp generator thread
    temp = 80
    temp_generator_thread = threading.Thread(target=temp_generator, args=(d,400,60,10,))
    temp_generator_thread.start()

    time.sleep(30)
    exit()