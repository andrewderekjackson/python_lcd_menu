
import Image, ImageFont, ImageDraw, textwrap

X_MAX = 320
Y_MAX = 240
OFFSET = 30

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# TFT configuration
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

class LcdDisplayController(object):


    def __init__(self):

        # Initialize display.
        self.disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
        self.disp.begin()

        self.current_dir = os.path.dirname(os.path.realpath(__file__))

        self.font = ImageFont.truetype(self.current_dir + "/arial.ttf", 18)
        self.font_large = ImageFont.truetype(self.current_dir + "/arial.ttf", 26)

        self.cover = Image.open(self.current_dir + "/wood.jpg")
        self.cover.thumbnail((X_MAX, Y_MAX))

        return super(LcdDisplayController, self).__init__()

    def draw_centered_text(self, text, font, fill=(255,255,255)):

        # Create a new image with transparent background to store the text.
        textimage = Image.new('RGBA', (X_MAX, Y_MAX), (0,0,0,0))
        textdraw = ImageDraw.Draw(textimage)

        lines = textwrap.wrap(text, width=25)
        y_text = 0
        for line in lines:
            text_width, text_height = font.getsize(line)
            textdraw.text((X_MAX/2-text_width/2, y_text), line, font=font, fill=fill)
            y_text += text_height

        return (textimage, X_MAX, y_text)

    def update(self, menu):

        image = Image.new("RGBA", (X_MAX, Y_MAX))
        image.paste(self.cover, (0, 0))

        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:

                text_image, width, height = self.draw_centered_text(item.title, self.font_large)
                # image.paste(text_image, (0,0), text_image)
                image.paste(text_image, (0, Y_MAX/2-height/2-OFFSET), text_image)

                text_image, width, height = self.draw_centered_text("(" + str(index+1) + "/" + str(len(menu.items)) + ")", self.font)
                image.paste(text_image, (X_MAX/2-width/2, Y_MAX-OFFSET), text_image)

        self.disp.display(image.rotate(90))

        #image.format = "PNG"
        #image.save("d:/temp/foo.png")


