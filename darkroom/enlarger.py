#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from threading import Thread

from gpiozero import OutputDevice


class Enlarger(OutputDevice):
    def __init__(self, pin, active_high=True):
        super(Enlarger, self).__init__(pin, active_high=active_high, initial_value=True)
        self.printing = False
        self.print_thread = None
        self.timer_thread = None
        self.draw = None
        self.state = False
        self.length = 0
        self.active_high = active_high
        self.off()

    def toggle(self):
        if self.printing:
            return False
        if self.state:
            self.off()
        else:
            self.on()

    def on(self):
        self.state = True
        super().on()

    def off(self):
        self.state = False
        super().off()

    def execute(self, length, draw):
        if self.printing:
            return False
        self.printing = True
        self.draw = draw
        self.length = length
        self.timer_thread = Thread(target=self._timer)
        self.print_thread = Thread(target=self._print_off)
        self.print_thread.setDaemon(True)
        self.timer_thread.setDaemon(True)
        self.print_thread.start()
        self.timer_thread.start()

    def _timer(self):
        initial = self.length
        while self.length > 0:
            self.draw(self.length)
            if not self.printing:
                self.draw(initial)
                return
            time.sleep(0.2)
        self.draw(initial)

    def _print_off(self):
        self.on()
        end_time = time.time() + self.length
        while self.length > 0:
            if not self.printing:
                return
            time.sleep(0.05)
            self.length -= 0.05
            if time.time() >= end_time:
                break
        self.printing = False
        self.off()
        self.length = 0

    def cancel(self):
        self.off()
        self.printing = False
        self.print_thread = None
        self.timer_thread = False
        self.length = 0
