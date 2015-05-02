import os

class ConsoleDisplayController(object):

    def update(self, menu):

        os.system('cls')
        
        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:
                print ">> " + item.title + " <<"
            else:
                print "   " + item.title


import Image, ImageFont, ImageDraw, textwrap

X_MAX = 320
Y_MAX = 240
OFFSET = 30

class LcdDisplayController(ConsoleDisplayController):
    

    def __init__(self):
        # self.font = ImageFont.load_default()
        self.font = ImageFont.truetype("micross.ttf", 18)
        self.font_large = ImageFont.truetype("micross.ttf", 24)
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
        super(LcdDisplayController, self).update(menu)

        image = Image.new("RGBA", (X_MAX, Y_MAX), "black")

        for (index, item) in enumerate(menu.items):
            if index == menu.selected_index:

                text_image, width, height = self.draw_centered_text(item.title, self.font_large)
                # image.paste(text_image, (0,0), text_image)
                image.paste(text_image, (0, Y_MAX/2-height/2-OFFSET), text_image)

                text_image, width, height = self.draw_centered_text("(" + str(index+1) + "/" + str(len(menu.items)) + ")", self.font)
                image.paste(text_image, (X_MAX/2-width/2, Y_MAX-OFFSET), text_image)
        
        image.format = "PNG"
        image.save("d:/temp/foo.png")

       
