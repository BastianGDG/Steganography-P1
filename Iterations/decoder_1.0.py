from PIL import Image
from bitarray import bitarray

img = Image.open("sample_new.bmp")

img2 = Image.open("green.bmp")

bits = []

dimensions = img.size

width = dimensions[0]

height = dimensions[1]

pixels = img.load()

pixels2 = img2.load()

for i in range(width):
    for j in range(height):
            RGB = pixels[i, j]

            R = RGB[0]
            G = RGB[1]
            B = RGB[2]

            RGB2 = pixels2[i, j]

            R2 = RGB2[0]
            G2 = RGB2[1]
            B2 = RGB2[2]

            if R2 == (R - 1) % 256:
                print(R, R2)
                bits.append("0")
            if R2 == (R + 1) % 256:
                print(R, R2)
                bits.append("1")
            else:
                pass

            if G2 == (G - 1) % 256:
                print(G, G2)
                bits.append("0")
            if G2 == (G + 1) % 256:
                print(G, G2)
                bits.append("1") 
            else:
                pass

            if B2 == (B - 1) % 256:
                print(B, B2)
                bits.append("0")
            if B2 == (B + 1) % 256:
                print(B, B2)
                bits.append("1")
            else:
                pass

full_bytes = [''.join(bits[i:i+8]) for i in range(0, len(bits) - (len(bits) % 8), 8)]

print(full_bytes)  

text = ''.join(chr(int(b, 2)) for b in full_bytes)
print(text)



