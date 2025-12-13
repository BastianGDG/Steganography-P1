from PIL import Image
from bitarray import bitarray

img = Image.open("green.bmp")

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

print("bytes er", bytes)

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
                    if R <= 128:
                        R = (RGB[0] + 1) % 256
                        print("1")
                    else:
                        R = (RGB[0] - 1) % 256
                        print("1")
                else:
                    pass 
                
                if bytes[0] == '0':
                    if R <= 128:
                        R = (RGB[0] + 2) % 256
                        print("0")
                    else:
                        R = (RGB[0] - 2) % 256
                        print("0")
                else:
                    pass

                # Green

                if bytes[1] == '1':
                    if G <= 128:
                        G = (RGB[1] + 1) % 256
                        print("1")
                    else:
                        G = (RGB[1] - 1) % 256
                        print("1")
                else:
                    pass 

                if bytes[1] == '0':
                    if G <= 128:
                        G = (RGB[1] + 2) % 256
                        print("0")
                    else:
                        G = (RGB[1] - 2) % 256
                        print("0")
                else:
                    pass
                
                # Blue

                if bytes[2] == '1':
                    if B <= 128:
                        B = (RGB[2] + 1) % 256
                        print("1")
                    else:
                        B = (RGB[2] - 1) % 256
                        print("1")
                else:
                    pass 
                
                if bytes[2] == '0':
                    if B <= 128:
                        B = (RGB[2] + 2) % 256
                        print("0")
                    else:
                        B = (RGB[2] - 2) % 256
                        print("0")
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
