# for menu
import threading
from lcd_menu import Command, MenuItem, Menu

import os
from time import time

# Rotary encoder
from rotary_encoder import RotaryEncoder
from lcd import Lcd

ROTARY_PIN_A = 14  # Pin 8
ROTARY_PIN_B = 15  # Pin 10
ROTARY_BUTTON = 4  # Pin 7


class RadioMenu(Menu):
    '''An example menu which received input from keyboard and outputs to a ILI9341 TFT display.'''

    MAIN_TITLE = "Internet Radio"

    def __init__(self, lcd):

        self.lcd = lcd
        self.rotary_encoder = RotaryEncoder(ROTARY_PIN_A, ROTARY_PIN_B, ROTARY_BUTTON, self.rotary_encoder_event)

        # our example menu definition
        items = [
            MenuItem("Playlists", refresh_callback=self.load_playlists),
            Command("Testing", self.do_thing),
            MenuItem("Radio", [
                MenuItem("Radio Station 1"),
                MenuItem("Radio Station 2"),
                MenuItem("Radio Station 3")
            ]),
            MenuItem("Settings", [
                MenuItem("IP Address"),
                MenuItem("Shutdown"),
            ]),
            Command("Volume UP", self.volume_up),
            Command("Volume DOWN", self.volume_down)
        ]

        # pass all this to the base class
        return super(RadioMenu, self).__init__(items, self.update)

    def rotary_encoder_event(self, event):

        if event == RotaryEncoder.CLOCKWISE:
            if self.showing_menu:
                print "MENU: DOWN"
                self.down()
            else:
                print "VOLUME: UP"
        elif event == RotaryEncoder.ANTICLOCKWISE:
            if self.showing_menu:
                print "MENU: UP"
                self.up()
            else:
                print "VOLUME: DOWN"
        elif event == RotaryEncoder.BUTTON_PRESSED:
            if self.showing_menu:
                print "MENU: SELECT"
                self.select()
            else:
                self.lcd.message2(RadioMenu.MAIN_TITLE, "Loading playlist...")
                print "PLAY/PAUSE"

        elif event == RotaryEncoder.BUTTON_LONG_PRESSED:
            if self.showing_menu:
                print "MENU: BACK"
                self.back()
            else:
                print "MENU: SHOW"
                self.show()

        return

    def loop(self):
        '''Main application loop. Receives input and dispatches one of either "up", "down", "select" or "back" commands.'''

        # display initial menu
        self.update(self.current_menu)

        while True:
            pass

    def update(self, menu):

        # show the "home" screen
        if not self.showing_menu:
            #self.message2(RadioMenu.MAIN_TITLE, "Short press to start playing now or long press for menu")

            self.lcd.message2(RadioMenu.MAIN_TITLE, "Starting up...")
            return

        # draw the current menu
        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:
                self.lcd.draw_menu(item.title, index, len(menu.items))

    def do_thing(self, item, arg):
        self.lcd.flash(str(time()), callback=self.close, interval=2)

    def volume_up(self, item, arg):
        print "RUNNING COMMAND: VOLUME UP"

    def volume_down(self, item, arg):
        print "RUNNING COMMAND: VOLUME DOWN"

    def on_play(self, item, arg):
        print "RUNNING COMMAND: PLAY: " + item.title

    def load_playlists(self, item, arg):
        '''Example of a dynamic menu item callback'''

        items = []

        items.append(Command("Andrew's Fairly Long Playlist", self.on_play))
        items.append(Command("Dynamic 2", self.on_play))
        items.append(Command("Dynamic 3", self.on_play))
        items.append(Command("Dynamic 4", self.on_play))

        for i in range(4, 10):
            items.append(Command("Dynamic " + str(i), self.on_play))

        return items


lcd = Lcd()

radioMenu = RadioMenu(lcd)
radioMenu.loop()
