import os
import termios
import sys
import tty
import time
import math


MODE_STBY = 1

class Controller:
    def __init__(self, display, enlarger):
        self.mode = MODE_STBY
        self.display = display
        self.enlarger = enlarger
        self.timer = 0.0
        self.set_timer_mode = False
        self.set_timer_capture = ""

    def start(self):
        self.main_loop();
    
    def main_loop(self):
        try:
            while True:
                char = self.get_char()
                ascii_char = ord(char)

                if ascii_char == 3 or char.lower() == "e":  # CTRL-C, "exit"
                    break

                elif ascii_char == 27:
                    self.display.write("NUMLK")
                    [self.get_char() for _ in range(2)]
                    continue
                elif ascii_char == 126:  # Not pressing numlock, maybe key
                    continue

                elif ascii_char == 13:
                    char = "enter"
                elif ascii_char == 127:
                    char = "backspace"
                elif char not in "0123456789.*/-+":
                    continue

                self.on_release(char)
        finally:
            self.display.write("------")
    
    def change_mode(self, mode):
        self.mode = mode
        self.refresh_mode()
    
    def refresh_mode(self):
        if self.mode == MODE_STBY:
            self.display.write(">")

    def get_char(self):
        stdin_file_descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(stdin_file_descriptor)
        try:
            tty.setraw(stdin_file_descriptor)
            character = sys.stdin.read(1)
        finally:
            termios.tcsetattr(stdin_file_descriptor, termios.TCSADRAIN, old_settings)
        return character

    def on_release(self, key):
        actions = {
            "enter": self.print_light,
            "/": self.enlarger.toggle,
            "backspace": self.cancel,
            "*": self.set_timer_mode_toggle,
            "+": self.add,
            "-": self.rem
        }

        if key == "backspace":
            self.cancel()
            return

        if self.enlarger.printing:
            if key == "enter":
                self.cancel()
            return

        if key in actions:
            return actions[key]()

        if self.set_timer_mode:
            if key in ".0123456789":
                self.set_timer_capture += key
                self.display.write(self.set_timer_capture + "*")
                return
            elif key in ".,":
                self.set_timer_capture += "."
                self.display.write(self.set_timer_capture + "*")
                return
            elif key == "enter" or key == "*":
                self.set_timer_mode_toggle()
                return
            else:
                try:
                    key.char
                except AttributeError:
                    pass
                else:
                    if str(key.char).startswith("5") or key.char is None:
                        set_timer_capture += "5"
                        self.display.write(set_timer_capture + "*")
                        return
        elif key in actions:
            return actions[key]()
    
    def cancel(self):
        self.enlarger.cancel()
        self.set_timer_mode = False
        self.display_time(self.timer)
        self.set_timer_capture = ""

    def add(self, amount=0.1):        
        self.timer = round(self.timer * math.pow(2, 1/6), 1)
        self.display_time(self.timer)


    def rem(self, amount=0.1):
        self.timer = round(self.timer / math.pow(2, 1/6), 1)
        self.display_time(self.timer)
    
    def display_time(self, number):
        self.display.write("{:.1f}".format(number).zfill(4))


    def print_light(self):
        self.enlarger.execute(self.timer, draw=self.display_time)

    def set_timer_mode_toggle(self):
        if self.set_timer_mode:
            try:
                new_timer = float(self.set_timer_capture)
            except ValueError as err:
                print("Bad timer value {}".format(err))
                set_timer_capture = ""
                self.display.write("ERROR")
                time.sleep(1)
                self.display_time(self.timer)
                return
            else:
                set_timer_capture = ""
                if 100 > new_timer >= 0:
                    self.timer = new_timer
                    self.display_time(self.timer)
                else:
                    self.display.write("ERROR")
                    time.sleep(1)
                    self.display_time(self.timer)
                    print("Bad timer value: {}".format(new_timer))
        else:
            self.display.write("Enter:")
        self.set_timer_mode = not self.set_timer_mode