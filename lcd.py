
# Screen dimentions
import threading

X_MAX = 320
Y_MAX = 240
OFFSET = 30

# TFT configuration
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

# for PIL
import Image, ImageFont, ImageDraw, textwrap, os

# TFT libraries
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI


class Lcd(object):

    def __init__(self):
        # Initialize display.
        self.disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
        self.disp.begin()

        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.message_timer = None

        # load the fonts
        self.font = ImageFont.truetype(self.current_dir + "/arial.ttf", 18)
        self.font_large = ImageFont.truetype(self.current_dir + "/ttwpgott.ttf", 34)

    def draw_menu(self, title, current_item, total_items):

        image = Image.new("RGBA", (X_MAX, Y_MAX))

        text_image, width, height = self.draw_centered_text(title, self.font_large)
        image.paste(text_image, (0, Y_MAX / 2 - height / 2 - OFFSET), text_image)

        text_image, width, height = self.draw_centered_text(
            "(" + str(current_item + 1) + "/" + str(total_items) + ")", self.font)
        image.paste(text_image, (X_MAX / 2 - width / 2, Y_MAX - OFFSET), text_image)

        self.disp.display(image.rotate(90))


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

    def message(self, message_string):
        image = self._create_message(message_string)
        self.disp.display(image.rotate(90))

    def message2(self, primary_text, secondary_text):
        image = Image.new("RGBA", (X_MAX, Y_MAX))

        text_image, width, height = self.draw_centered_text(primary_text, self.font_large)
        image.paste(text_image, (0, Y_MAX / 2 - height / 2 - OFFSET), text_image)

        text_image, width, height = self.draw_centered_text(secondary_text, self.font)
        image.paste(text_image, (0, Y_MAX - 70 - height/2), text_image)

        self.disp.display(image.rotate(90))

    def flash(self, message_string, callback, interval=3):

        if self.message_timer is not None:
            self.message_timer.cancel()
            self.message_timer = None

        image = self._create_message(message_string)
        self.disp.display(image.rotate(90))

        self.message_timer = threading.Timer(interval, callback)
        self.message_timer.start()

    def _create_message(self, message_string):

        image = Image.new("RGBA", (X_MAX, Y_MAX))

        text_image, width, height = self.draw_centered_text(message_string, self.font_large)
        image.paste(text_image, (0, Y_MAX / 2 - height / 2 - OFFSET), text_image)

        return image