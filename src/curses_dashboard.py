#!/usr/bin/python3

import curses
import time
from curses import wrapper

from tach import Tach
from gear import Gear
from throttle import Throttle
from cht import Cht
from temp_sensor import TempSensor
from gps import Gps
import board
from accel import Accelerometer

# set up curses
stdscr = curses.initscr()
curses.noecho()
stdscr.nodelay(True)
curses.cbreak()

# initialize sensors
# TODO:  wrap in try/except's
tach = Tach()
gear = Gear()
throttle = Throttle()
cht = TempSensor(board.D5)
egt = TempSensor(board.D6)
gps = Gps()
accel = Accelerometer()

# The number of times per second the dash refreshes
refresh_rate = 5

temp_iterator = 0
last_cht = cht.temperature()
cht_delta = 0
last_egt = egt.temperature()
egt_delta = 0

while True:
    stdscr.addstr(0,0,  f"RPM's: {tach.rpms():6.0f}")
    stdscr.addstr(0,16, f"MPH:   {gps.speed():3.0f}")

    stdscr.addstr(1,16, f"Gear:    {gear.gear()}")
    stdscr.addstr(1,0,  f"Throttle: {throttle.percent():3.0f}%")
    
    stdscr.addstr(3,0, "Temps (F):")

    cht_temp = cht.temperature()
    egt_temp = egt.temperature()

    if temp_iterator % refresh_rate == 0:
        cht_delta =  cht_temp - last_cht
        if cht_delta < 1:
            cht_delta = 0
        egt_delta =  egt_temp - last_egt
        if egt_delta < 1:
            egt_delta = 0
        temp_iterator = 0
    else:
        temp_iterator += 1

    if cht_temp == 32:
        stdscr.addstr(4,0, "CHT:   -")
    else:
        stdscr.addstr(4,0, f"CHT: {cht_temp:3.0f} {cht_delta:+5.1f}")

    if egt_temp == 32:
        stdscr.addstr(4,16, "EGT:   -")
    else:
        stdscr.addstr(4,16, f"EGT:  {egt_temp:3.0f} {'+' if egt_delta >= 0 else ''}{egt_delta:+5.1f}")

    stdscr.addstr(6,0, "Acceleration:")
    stdscr.addstr(7,0, f"x: {accel.x():04.2f}")
    stdscr.addstr(7,9, f"y: {accel.y():04.2f}")
    stdscr.addstr(7,18, f"z: {accel.z():04.2f}")

    try:
        k = stdscr.getkey()
        if k == "q":
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

            exit()


    except Exception:
        pass

    stdscr.refresh()
    time.sleep(.2)

time.sleep(5)
# shutdown
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()


def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
