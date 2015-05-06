# for menu
import threading
from lcd_menu import Command, MenuItem, Menu

import os, time

# for PIL
import Image, ImageFont, ImageDraw, textwrap

# TFT libraries
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

from rotary_encoder import RotaryEncoder

# Screen dimentions
X_MAX = 320
Y_MAX = 240
OFFSET = 30

# TFT configuration
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Rotary encoder
ROTARY_PIN_A = 14  # Pin 8
ROTARY_PIN_B = 15  # Pin 10
ROTARY_BUTTON = 4  # Pin 7

# import gaugette.rotary_encoder


class RadioMenu(Menu):
    '''An example menu which received input from keyboard and outputs to a ILI9341 TFT display.'''

    def __init__(self):

        # Initialize display.
        self.disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
        self.disp.begin()

        # Initialize rotary encoder
        self.rotary_encoder = RotaryEncoder(ROTARY_PIN_A, ROTARY_PIN_B, ROTARY_BUTTON, self.rotary_encoder_event)

        self.current_dir = os.path.dirname(os.path.realpath(__file__))

        self.font = ImageFont.truetype(self.current_dir + "/arial.ttf", 18)
        self.font_large = ImageFont.truetype(self.current_dir + "/arial.ttf", 26)

        # our example menu definition
        items = [
            MenuItem("Playlists", refresh_callback=self.load_playlists),
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
            print "REC: CLOCKWISE"
            self.down()
        elif event == RotaryEncoder.ANTICLOCKWISE:
            print "REC: ANTICLOCKWISE"
            self.up()
        elif event == RotaryEncoder.BUTTON_PRESSED:
            print "REC: BUTTON_PRESSED"
            self.select()
        elif event == RotaryEncoder.BUTTON_LONG_PRESSED:
            print "REC: BUTTON_LONG_PRESSED"
            self.back()

        return

    def loop(self):
        '''Main application loop. Receives input and dispatches one of either "up", "down", "select" or "back" commands.'''

        # display initial menu
        self.update(self.current_menu)

        while True:
            pass

        # self.rotary_encoder.start()
        #
        # last_delta = 0
        # while True:
        #
        #     delta = self.rotary_encoder.get_delta()
        #
        #     if delta != 0:
        #         last_delta += delta
        #
        #         if last_delta%4 == 0:
        #             if delta == 1:
        #                 self.down()
        #             if delta == -1:
        #                 self.up()

        #    print ("rotate %d" % delta)

        # if delta == -1:
        #     print "ANTICLOCKWISE"
        #     #self.up()
        #
        # if delta == 1:
        #     print "CLOCKWISE"
        #     #self.down()



    def draw_centered_text(self, text, font, fill=(255, 255, 255)):

        # Create a new image with transparent background to store the text.
        textimage = Image.new('RGBA', (X_MAX, Y_MAX), (0, 0, 0, 0))
        textdraw = ImageDraw.Draw(textimage)

        lines = textwrap.wrap(text, width=25)
        y_text = 0
        for line in lines:
            text_width, text_height = font.getsize(line)
            textdraw.text((X_MAX / 2 - text_width / 2, y_text), line, font=font, fill=fill)
            y_text += text_height

        return (textimage, X_MAX, y_text)

    def update(self, menu):

        image = Image.new("RGBA", (X_MAX, Y_MAX))

        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:
                text_image, width, height = self.draw_centered_text(item.title, self.font_large)
                # image.paste(text_image, (0,0), text_image)
                image.paste(text_image, (0, Y_MAX / 2 - height / 2 - OFFSET), text_image)

                text_image, width, height = self.draw_centered_text(
                    "(" + str(index + 1) + "/" + str(len(menu.items)) + ")", self.font)
                image.paste(text_image, (X_MAX / 2 - width / 2, Y_MAX - OFFSET), text_image)

        self.disp.display(image.rotate(90))


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


radioMenu = RadioMenu()
radioMenu.loop()
