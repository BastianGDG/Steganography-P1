from PIL import Image
from bitarray import bitarray

img = Image.open("sample.bmp")

string = input("Skriv det du vil embedde:")

ba = bitarray()

ba.frombytes(string.encode())

print(ba.to01()) 

print(img.format, img.size, img.mode)

bits = ba.to01()

bytes = []

print(bits)

dimensions = img.size

n = 0

width = dimensions[0]

height = dimensions[1]

pixels = img.load()

for i, bit in enumerate(bits):
 
    bytes.append(bit)

    if (i + 1) % 8 == 0 and i < len(bits) - 1:
        bytes.append(" ")
        
bytes.append(" ")

for i in range(8):
    bytes.append("0")

while len(bytes) % 3 != 0:
    bytes.append("")

if width * height * 3 > len(bytes):
    for i in range(width):
        for j in range(height):
            RGB = pixels[i, j]

            R = RGB[0]
            G = RGB[1]
            B = RGB[2]

            if len(bytes) > 0:
                # Red
                if bytes[0] == '1':
                        R = (RGB[0] + 1) % 256
                else:
                    pass 
                
                if bytes[0] == '0':
                        R = (RGB[0] - 1) % 256
                else:
                    pass

                # Green

                if bytes[1] == '1':
                        G = (RGB[1] + 1) % 256
                else:
                    pass 

                if bytes[1] == '0':
                        G = (RGB[1] - 1) % 256
                else:
                    pass
                
                # Blue

                if bytes[2] == '1':
                        B = (RGB[2] + 1) % 256
                else:
                    pass 
                
                if bytes[2] == '0':
                        B = (RGB[2] - 1) % 256
                else:
                    pass
   
            else:
                break
            
            pixels[i, j] = (R,G,B) 

            if len(bytes) > 0:
                bytes = bytes[1:]

            if len(bytes) > 0:
                bytes = bytes[1:]

            if len(bytes) > 0:    
                bytes = bytes[1:]


else:
    print("Your image is too small!")

img.save("sample_new.bmp")

print(bytes)
print(pixels[0, 0], width, height)  
