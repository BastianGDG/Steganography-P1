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

lsb = []

print(bits)

dimensions = img.size

count = 0

n = 0

width = dimensions[0]

height = dimensions[1]

pixels = img.load()

for i, bit in enumerate(bits):
 
    bytes.append(bit)
        
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
                
                #RED

                binary = bin(RGB[0])

                for character in binary:
    
                    lsb.append(character)

                print("before", lsb)

                if bytes[0] != lsb[len(lsb)-1]:
                    lsb[-1] = int(lsb[-1])
                    lsb[-1] = (lsb[-1] + 1) % 2
                    lsb[-1] = str(lsb[-1])

                print("after", lsb)
                
                count += 1
                print(count)

                result = ''.join(lsb)

                k = int(result, 2)

                R = k % 256

                result = ''
                lsb = []

                #GREEN

                binary = bin(RGB[1])

                for character in binary:
    
                    lsb.append(character)

                print("before", lsb)

                if bytes[1] != lsb[len(lsb)-1]:
                    lsb[-1] = int(lsb[-1])
                    lsb[-1] = (lsb[-1] + 1) % 2
                    lsb[-1] = str(lsb[-1])

                print("after", lsb)
                
                count += 1
                print(count)

                result = ''.join(lsb)

                k = int(result, 2)

                G = k % 256

                result = ''
                lsb = []

                #BLUE

                binary = bin(RGB[2])

                for character in binary:
    
                    lsb.append(character)

                print("before", lsb)

                if bytes[2] != lsb[len(lsb)-1]:
                    lsb[-1] = int(lsb[-1])
                    lsb[-1] = (lsb[-1] + 1) % 2
                    lsb[-1] = str(lsb[-1])

                print("after", lsb)
                
                count += 1
                print(count)

                result = ''.join(lsb)

                k = int(result, 2)

                B = k % 256

                result = ''
                lsb = []

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
