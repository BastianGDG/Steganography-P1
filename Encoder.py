from PIL import Image
from bitarray import bitarray

img = Image.open("sample.bmp")

class ImageHandler:
    def __init__(self, currentPixel, bytes):
        self.currentPixel = currentPixel
        self.bytes = bytes
        self.dimensions = img.size
    
    def stringToBytes(self, bytes):
        # En funktion som konveterer en string "Hello World" til bytes "0011011 00010110"
        pass

    def addSpacing(self, bytes):
        # En fuktion som tilføjer mellemrum mellem hver byte, det skal ske hver 8. bit
        pass

    def addPadding(self, bytes):
        # En funktion som tilføjer padding så længden af byte array'et er dividerbar med 3
        pass