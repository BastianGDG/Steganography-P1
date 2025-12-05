from PIL import Image
from bitarray import bitarray
from tkinter import Tk, filedialog
from pathlib import Path
import base64
import os
import time

def main():
    # Asks the user for a file to embed using the openFile() function
    FILE_path = openFile()
    # If the user selected nothing, the program ends
    if FILE_path is None:
        return
    
    # Opens the file in "Read, Binary (rb)" mode
    with open(FILE_path, "rb") as FILE:
    # Reads the file and gives the content to the message variable
        message = FILE.read()

    # Gets the filename and extention of the given file
    filename = os.path.basename(FILE_path)

    # Converts the file content to base64 (This makes it MUCH easier to handle, as raw file contents are tricky), 
    # the .decode at the end ensures that we get it as string
    message = base64.b64encode(message).decode()

    # Gets the length of filename (Counting each character) 
    filenameLength = len(filename)

    # Initialize bitarrays using bitarray library, and convert message to binary
    ba_message = bitarray()

    #This converts the message into binary, it's data type is a string
    ba_message.frombytes(message.encode())
    messageBits = ba_message.to01()

    # Same logic but we're converting the base64 encoded file contents to binary
    ba_file = bitarray()

    ba_file.frombytes(filename.encode())
    filenameBits = ba_file.to01()

    # Same logic but we're converting the filenameLength to binary
    ba_ext = bitarray()
    ba_ext.frombytes(bytes([filenameLength])) 
    extensionBits = ba_ext.to01()

    #Array to contain the bits from above, we dont want them in string form
    arrayOfBits = []

    # User chooses their file (The image choosing logic is irrelevant, dont waste your time trying to understand it)
    IMAGE_path = openImage()
    if IMAGE_path is None:
        return

    # Image object
    IMAGE = Image.open(IMAGE_path)  

    # Runs the stringToArray function, with the initialized variables
    stringToArray(arrayOfBits, messageBits, filenameBits, extensionBits, IMAGE, IMAGE_path)

def openFile():
    # This function can be ignored
    # Hides the main window
    root = Tk()
    root.withdraw()
    # Opens file dialoge
    FILE = filedialog.askopenfilename(
        title="Choose a file to embed",
        filetypes=[("All files", "*.*")]
    )
    if FILE:
        print("Chosen file:", FILE)
        return FILE
    else:
        print("No file chosen")
        return None

def openImage():
    # This function can be ignored
    # Hides the main window
    root = Tk()
    root.withdraw()
    # Opens file dialoge
    IMAGE = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
    )
    if IMAGE:
        print("Chosen file:", IMAGE)
        return IMAGE
    else:
        print("No file chosen")
        return None

def stringToArray(arrayOfBits, messageBits, filenameBits, extensionBits, IMAGE, IMAGE_path):

    # This ensures that we always have 8 bits (1 byte) of space allocated to containing the filenameLength 
    # (Just the length, not the filename itself)
    # The reason we're doing this is because the decoder doesn't know when to stop looking for this number, unless we have a fixed value in both ends
    while len(extensionBits) < 8:
        extensionBits += "0"

    # Adds the 8 bits of extentionLength to our collective bit array
    for bit in extensionBits:
        arrayOfBits.append(bit)

    # Adds the bits that describe the filename to the collective bit array
    for bit in filenameBits:
        arrayOfBits.append(bit)

    # For loop that iterates through every element in the messageBits, and inserts them into our array
    for bit in messageBits:
        arrayOfBits.append(bit)

    # For loop that adds the null terminator ( Spørg Bastian hvad en null terminator er :D )    
    for _ in range(8):
        arrayOfBits.append("0")

    # Our arrayOfBits now looks something like this: [{fileNameLength}, {fileName}, {File contents}, {Null terminator}]

    addPadding(arrayOfBits, IMAGE, IMAGE_path)


def addPadding(arrayOfBits, IMAGE, IMAGE_path):
    # For loop that adds padding to the array so that it's length is a multiple of 3, this is because there are 3 RGB values
    while len(arrayOfBits) % 3 != 0:
        arrayOfBits.append("")

    shiftPixels(arrayOfBits, IMAGE, IMAGE_path)


def shiftPixels(arrayOfBits, IMAGE, IMAGE_path):
    #Loads image into pixel variable, this will be used to handle invidiual pixels
    pixel = IMAGE.load()

    #Get image dimensions, width and length
    dimensions = IMAGE.size

    # Defines the length of the arrayOfBits before we start removing contents from it
    # Dont look too much into this, it's just for the fancy % loader
    encodingLength = len(arrayOfBits)
    last_progress = 101

    # This starts the timer so that we may record how many bits per second we're encoding
    # It's irrelevant to stego
    start_time = time.time()

    # Counter to keep track of the current bit we're encoding
    counter = int(0)

    # Checks if the image is big enough to contain the given message 
    # The formula for calculating the max. data size to embed is (image width * image height * 3) (because there are 3 RGB values)
    if dimensions[0] * dimensions[1] * 3 > len(arrayOfBits):
        print("Starting encoding...")
        # Nested for loops that iterate through every pixel in the image, starts from top left corner (0,0) to bottom right corner
        for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                for n in range(3):
                    # Grabs the current pixel's RGB values
                    RGB = pixel[i, j]

                    #Checks if theres any Bits left to encode, if not it breaks the loop, no need to keep looking
                    if len(arrayOfBits) > counter:
                        currentBit = arrayOfBits[counter]

                        # Variable to keep track of the current RGB value used, we can only use one at a time R, G, B (Ja jeg er meget god til navngiving)
                        rgb = RGB[n]

                        # Placeholder variables, result is to hold the binary value as a string, the other to hold it as an array
                        stringPlaceholder = ''
                        LSB = []

                        # Converts the current RGB value to binary
                        binaryColorValue = bin(rgb)

                        # Goes through every bit in the binary RGB value, and appends it to the lsb array
                        for character in binaryColorValue:
                            LSB.append(character)

                        # Logikken under er en del kringlet, forstå så godt som du kan, spørg mig 
                        # Checks if the Current bit we're encoding, matches the last (least significant bit) bit of the RGB value
                        if currentBit != LSB[-1]:
                            # Converts the last bit to an integer so that we may do math to it-
                            # (saying lsb[-1] takes the last element of the array)
                            # Adds one so that it matches the bit we're encoding, and takes modulus 2, so that it's always either a 1 or 0
                            LSB[-1] = (int(LSB[-1]) + 1) % 2

                            # Converts back to string so that we can parse it
                            LSB[-1] = str(LSB[-1])
                           
                        # Converts the lsb array into a string
                        stringPlaceholder = ''.join(LSB)

                        # Converts the binary string in result back to an integer
                        k = int(stringPlaceholder, 2)

                        # Sets the new R, G or B value to be encoded
                        rgb = k % 256

                        # Changes the RGB value dependent on which RGB value we currently are on (Yes this logic can probably be improved upon)
                        if n == 0:
                            pixel[i, j] = (rgb, RGB[1], RGB[2])
                        elif n == 1:
                            pixel[i, j] = (RGB[0], rgb, RGB[2])
                        elif n == 2:
                            pixel[i, j] = (RGB[0], RGB[1], rgb)

                        counter += 1

                        # This is for the % loader and bits per second, when encoding, its irrelevant to stego
                        # The program is pretty slow, so having a percentage helps
                        progress = int((len(arrayOfBits) / (encodingLength - 1)) * 100)
                        progress = 100 - progress 
                        if progress != last_progress:
                            elapsed_time = time.time() - start_time
                            bits_encoded = encodingLength - len(arrayOfBits)
                            bits_per_second = bits_encoded / elapsed_time if elapsed_time > 0 else 0
                            print(f"\rEncoding {progress}% done - {bits_per_second:.0f} bits/s", end="")
                            last_progress = progress
                    else:
                        print("\nDone! \n")

                        # Saves the image
                        path = Path(IMAGE_path)
                        save_path = path.parent / f"enc_{path.name}"
                        IMAGE.save(save_path)
                        print("Image is saved as:", save_path)
                        return
    else:
        print("Your image is too small!")

main()
