import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class OledDisplay:

    def __init__(self):

        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.disp.begin()
        self.font = ImageFont.load_default()
        self.width = self.disp.width
        self.height = self.disp.height
        padding = -2
        self.top = padding
        self.bottom = self.height-padding
        self.left = 0
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        
    def clear(self):
        self.disp.clear()
        self.disp.display()
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def write_line(self, line, msg):

        self.draw.text((self.left, self.top + line * 8), msg,  font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

if __name__ == "__main__":

    ol = OledDisplay()
    ol.clear()

    ol.write_line(0, "Linha 1")
    ol.write_line(1, "Linha 2")
    ol.write_line(2, "Linha 3")
    ol.write_line(3, "Linha 4")

