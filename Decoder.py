from tkinter import Tk, filedialog
from pathlib import Path
from PIL import Image
import base64
from encryptdecrypt import decrypt

def main():
    # User chooses their file (The image choosing logic is irrelevant, dont waste your time trying to understand it)
    IMAGE_path = openImage()
    if IMAGE_path is None:
        return

    # Image object
    IMAGE = Image.open(IMAGE_path)  

    # Runs the code function with image as parameter
    decode(IMAGE)

def openImage():
    # This function can be ignored
    # Hides the main window
    root = Tk()
    root.withdraw()

    # Opens file dialoge
    IMAGE = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp"), ("All files", "*.*")]
    )

    if IMAGE:
        print("Chosen file:", IMAGE)
        return IMAGE
    else:
        print("No file chosen")
        return None

def decode(IMAGE):
    # Array to store the decoded bits
    bits = []
    
    # Grab dimensions of image
    dimensions = IMAGE.size
    
    # Grab pixel values
    pixel = IMAGE.load()

    #Initalize RGB value count
    currentRGBValue = 0
    
    count = 0

    extentionLength = 0

    filenameDecoded = False
    extentionLengthDecoded = False

    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            for n in range(3):
                RGB = pixel[i, j]
                if count < 8:     
                    # Placeholder array to hold the decoded bits so they can be added to the bit array
                    lsb = [] 

                    #Grabs the binary value of the current RGB value
                    rgb = bin(RGB[currentRGBValue])

                    #Goes through every bit in the binary value of the current RGB value and append to the lsb array
                    for character in rgb:
                        lsb.append(character)

                    # Takes the last bit of the lsb array and adds it to the decoded bits
                    bits.append(lsb[-1]) 
                    
                    count = count + 1

                    #Increments currentRGBvalue by 1, and also makes sure it stays between 0, 1 and 2, 0 = R, 1 = G, 2 = B
                    currentRGBValue = (currentRGBValue + 1) % 3 

                elif count == 8:
                    extentionLength = ''.join(bits)
                    extentionLength = int(extentionLength, 2) * 8
                    bits = []
                    extentionLengthDecoded = True
                
                if 8 <= count and count < extentionLength + 8 and extentionLengthDecoded == True and filenameDecoded == False:
                    RGB = pixel[i, j]
                    
                    # Placeholder array to hold the decoded bits so they can be added to the bit array
                    lsb = [] 

                    #Grabs the binary value of the current RGB value
                    rgb = bin(RGB[currentRGBValue])

                    #Goes through every bit in the binary value of the current RGB value and append to the lsb array
                    for character in rgb:
                        lsb.append(character)

                    # Takes the last bit of the lsb array and adds it to the decoded bits
                    bits.append(lsb[-1]) 
                    
                    count = count + 1

                    #Increments currentRGBvalue by 1, and also makes sure it stays between 0, 1 and 2, 0 = R, 1 = G, 2 = B
                    currentRGBValue = (currentRGBValue + 1) % 3 

                elif count >= extentionLength + 8 and extentionLengthDecoded == True and filenameDecoded == False:
                    # Adds spacing every 8 bit to split into bytes
                    full_bytes = [''.join(bits[k:k+8]) for k in range(0, len(bits) - (len(bits) % 8), 8)]
    
                    # Converts bytes into characters
                    fileName = ''.join(chr(int(b, 2)) for b in full_bytes)

                    filenameDecoded = True

                    bits = []

                if extentionLengthDecoded == True and filenameDecoded == True:
                    # Placeholder array to hold the decoded bits so they can be added to the bit array
                    lsb = [] 

                    #Grabs the binary value of the current RGB value
                    rgb = bin(RGB[currentRGBValue])

                     # Looks for the null terminator, "If the length of bits is greater than 8 and the last 8 elements are 0000000: Break,"
                    if len(bits) >= 8 and ''.join(bits[-8:]) == '00000000':
                            remakeFile(bits,fileName)
                            return None
                    else:
                            #Goes through every bit in the binary value of the current RGB value and append to the lsb array
                            for character in rgb:
                                lsb.append(character)
            
                            # Takes the last bit of the lsb array and adds it to the decoded bits
                            bits.append(lsb[-1]) 
                            
                            #Increments currentRGBvalue by 1, and also makes sure it stays between 0, 1 and 2, 0 = R, 1 = G, 2 = B
                            currentRGBValue = (currentRGBValue + 1) % 3 

def remakeFile(bits,fileName):

    password = input("Enter the password used (leave blank if none): ")

    # Adds spacing every 8 bit to split into bytes
    full_bytes = [''.join(bits[i:i+8]) for i in range(0, len(bits) - (len(bits) % 8), 8)]
    
    # Converts bytes into characters
    text = ''.join(chr(int(b, 2)) for b in full_bytes)

    file_bytes = base64.b64decode(text)

    if password:
        try:
            fileName = base64.b64decode(fileName)

            file_bytes = decrypt(file_bytes, password)

            fileName = decrypt(fileName, password)

            with open(fileName, "wb") as f:
                f.write(file_bytes)

                                
            print("Filename is:")
            print(fileName)

        except:
            print("Wrong password!!!")
    else:
        with open(fileName, "wb") as f:
            f.write(file_bytes)
                                
            print("Filename is:")
            print(fileName)

main()