from PIL import Image
from bitarray import bitarray

img = Image.open("enc_black.bmp")

bits = []

dimensions = img.size

width = dimensions[0]

height = dimensions[1]

pixels = img.load()

lsb = []

for i in range(width):
    for j in range(height):
            RGB = pixels[i, j]

            R = bin(RGB[0])
            G = bin(RGB[1])
            B = bin(RGB[2])

            if len(bits) >= 8 and ''.join(bits[-8:]) == '00000000':
                    break
            else:
                    for character in R:
                        lsb.append(character)

                    print("LSB:", lsb)
                    bits.append(lsb[-1])
                
                    lsb = []


            if len(bits) >= 8 and ''.join(bits[-8:]) == '00000000':
                    break
            else:                 
                    for character in G:
                        lsb.append(character)

                    print("LSB:", lsb)
                    bits.append(lsb[-1])

                    lsb = []

            if len(bits) >= 8 and ''.join(bits[-8:]) == '00000000':
                    break
            else:
                    for character in B:
                        lsb.append(character)

                    print("LSB:", lsb)
                    bits.append(lsb[-1])

                    lsb = []
                    

full_bytes = [''.join(bits[i:i+8]) for i in range(0, len(bits) - (len(bits) % 8), 8)]

print(full_bytes)  

text = ''.join(chr(int(b, 2)) for b in full_bytes)
print(text)



