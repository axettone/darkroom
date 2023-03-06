#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import termios
import sys
import tty
import time
import math

from PIL import ImageFont

from darkroom.dummy_enlarger import DummyEnlarger
from darkroom.display import Display
from darkroom.controller import Controller

X_OFFSET = int(os.getenv('X_OFFSET', 0))
Y_OFFSET = int(os.getenv('Y_OFFSET', -2))
BLOCK_DIR = int(os.getenv('BLOCK_DIR', -90))
ENLARGER_PIN = int(os.getenv('ENLARGER_PIN', 18))
STARTUP_MESSAGE = os.getenv('STARTUP_MESSAGE', 'LOVE U')
FONT_FILE = os.getenv('FONT_FILE', os.path.join(os.path.dirname(__file__), "fonts", "scoreboard.ttf"))
ACTIVE_MODE_HIGH = os.getenv('ACTIVE_MODE_HIGH', True)
STOP_INCREMENTS = os.getenv('STOP_INCREMENTS', False)

#font_path = os.path.abspath(FONT_FILE)

#font = ImageFont.truetype(font_path, 10)

#serial = spi(port=0, device=0, gpio=noop())
#device = max7219(serial, cascaded=4, block_orientation=BLOCK_DIR)




enlarger = DummyEnlarger(pin=ENLARGER_PIN, active_high=ACTIVE_MODE_HIGH)
display = Display()
controller = Controller(display, enlarger)


def main():
    controller.start()
    


if __name__ == "__main__":
    main()
