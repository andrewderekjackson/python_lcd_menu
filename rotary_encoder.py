#!/usr/bin/env python
#
# Raspberry Pi Rotary Encoder Class

# Original code from here:
#   https://github.com/guyc/py-gaugette/blob/master/gaugette/rotary_encoder.py

import RPi.GPIO as GPIO
import math
import threading
import time
import datetime


class RotaryEncoder:
    CLOCKWISE = 1
    ANTICLOCKWISE = 2
    BUTTON_PRESSED = 3
    BUTTON_LONG_PRESSED = 4

    LONG_PRESS_TIME = 0.3

    # Initialise rotary encoder object
    def __init__(self, pinA, pinB, button, callback):

        self.pinA = pinA
        self.pinB = pinB
        self.callback = callback

        self.timer = None
        self.button = button
        self.button_timer_elapsed = False

        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)
        GPIO.setup(self.pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.button, GPIO.BOTH, callback=self.button_event, bouncetime=50)

        self.last_delta = 0
        self.r_seq = self.rotation_sequence()

        # steps_per_cycle and remainder are only used in get_cycles which
        # returns a coarse-granularity step count.  By default
        # steps_per_cycle is 4 as there are 4 steps per
        # detent on my encoder, and get_cycles() will return -1 or 1
        # for each full detent step.
        self.steps_per_cycle = 4
        self.remainder = 0

        worker = threading.Thread(target=self.poll)
        worker.setDaemon(True)
        worker.start()

        return

    def poll(self):

        print "polling"

        last_delta = 0
        while True:

            delta = self.get_delta()

            if delta != 0:
                last_delta += delta

                if last_delta%4 == 0:
                    if delta == 1:
                        self.callback(RotaryEncoder.CLOCKWISE)
                    if delta == -1:
                        self.callback(RotaryEncoder.ANTICLOCKWISE)


        # Returns the quadrature encoder state converted into
        # a numerical sequence 0,1,2,3,0,1,2,3...
        #
        # Turning the encoder clockwise generates these
        # values for switches B and A:
        #  B A
        #  0 0
        #  0 1
        #  1 1
        #  1 0
        # We convert these to an ordinal sequence number by returning
        #   seq = (A ^ B) | B << 2
        #

    def rotation_sequence(self):
        a_state = GPIO.input(self.pinA)
        b_state = GPIO.input(self.pinB)
        r_seq = (a_state ^ b_state) | b_state << 1
        return r_seq

    # Returns offset values of -2,-1,0,1,2
    def get_delta(self):
        delta = 0
        r_seq = self.rotation_sequence()
        if r_seq != self.r_seq:
            delta = (r_seq - self.r_seq) % 4
            if delta==3:
                delta = -1
            elif delta==2:
                delta = int(math.copysign(delta, self.last_delta))  # same direction as previous, 2 steps

            self.last_delta = delta
            self.r_seq = r_seq

        return delta

    # get_cycles returns a scaled down step count to match (for example)
    # the detents on an encoder switch.  If you have 4 delta steps between
    # each detent, and you want to count only full detent steps, use
    # get_cycles() instead of get_delta().  It returns -1, 0 or 1.  If
    # you have 2 steps per detent, set encoder.steps_per_cycle to 2
    # before you call this method.
    def get_cycles(self):
        # python negative integers do not behave like they do in C.
        #   -1 // 2 = -1 (not 0)
        #   -1 % 2 =  1 (not -1)
        # // is integer division operator.  Note the behaviour of the / operator
        # when used on integers changed between python 2 and 3.
        # See http://www.python.org/dev/peps/pep-0238/
        self.remainder += self.get_delta()
        cycles = self.remainder // self.steps_per_cycle
        self.remainder %= self.steps_per_cycle # remainder always remains positive
        return cycles

    # # Call back routine called by switch events
    # def switch_event(self, switch):
    #     if GPIO.input(self.pinA):
    #         self.rotary_a = 1
    #     else:
    #         self.rotary_a = 0
    #
    #     if GPIO.input(self.pinB):
    #         self.rotary_b = 1
    #     else:
    #         self.rotary_b = 0
    #
    #     self.rotary_c = self.rotary_a ^ self.rotary_b
    #     new_state = self.rotary_a * 4 + self.rotary_b * 2 + self.rotary_c * 1
    #     delta = (new_state - self.last_state) % 4
    #     self.last_state = new_state
    #     event = 0
    #
    #     if delta == 1:
    #         if self.direction == self.CLOCKWISE:
    #             # print "Clockwise"
    #             event = self.direction
    #         else:
    #             self.direction = self.CLOCKWISE
    #     elif delta == 3:
    #         if self.direction == self.ANTICLOCKWISE:
    #             # print "Anticlockwise"
    #             event = self.direction
    #         else:
    #             self.direction = self.ANTICLOCKWISE
    #     if event > 0:
    #         self.callback(event)
    #     return

    def button_event(self, button):

        if GPIO.input(button):

            if self.timer is not None:
                self.timer.cancel()
                self.timer = None

            if self.button_timer_elapsed:
                self.button_timer_elapsed = False
                return

            self.callback(self.BUTTON_PRESSED)
        else:
            self.timer = threading.Timer(self.LONG_PRESS_TIME, self.on_timer)
            self.timer.start()

        return

    def on_timer(self):
        self.button_timer_elapsed = True
        self.callback(self.BUTTON_LONG_PRESSED)

