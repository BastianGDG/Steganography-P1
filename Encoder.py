from PIL import Image
from bitarray import bitarray
from tkinter import Tk, filedialog

def main():
    # User input
    message = input("Write what you would like to embed: ")

    # Initialize bitarrays using bitarray library, and convert message to binary
    bitArray = bitarray()
    bitArray.frombytes(message.encode())

    #This converts the message into binary, it's data type is a string
    bits = bitArray.to01()

    #Array to contain the bits from above, we dont want them in string form
    arrayOfBits = []

    IMAGE = openImage()
    
    #Runs the stringToArray function, with the initialized variables
    stringToArray(arrayOfBits, bits, IMAGE)

def openImage():
    # skjul hovedvinduet
    root = Tk()
    root.withdraw()

    # åbn file dialog
    IMAGE = filedialog.askopenfilename(
        title="Vælg et billede",
        filetypes=[("Billeder", "*.png *.jpg *.jpeg *.bmp"), ("Alle filer", "*.*")]
    )

    if IMAGE:
        print("Valgt fil:", IMAGE)
    else:
        print("Ingen fil valgt")

    return IMAGE

def stringToArray(arrayOfBits, bits, IMAGE):
    # For loop that iterates through every element in the bit string, and inserts them into our array
    for i, bit in enumerate(bits):
        arrayOfBits.append(bit)

    # For loop that adds the null terminator ( Spørg Bastian hvad en null terminator er :D )    
    for i in range(8):
        arrayOfBits.append("0")
    
    addPadding(arrayOfBits, IMAGE)
    

def addPadding(arrayOfBits, IMAGE):
    # For loop that adds padding to the array so that it's length is a multiple of 3, this is because there are 3 RGB values
    while len(arrayOfBits) % 3 != 0:
        arrayOfBits.append("")
    
    shiftPixels(arrayOfBits, IMAGE)
    

def shiftPixels(arrayOfBits, IMAGE):

    print(arrayOfBits)
    #Loads image into pixel variable, this will be used to handle invidiual pixels
    pixel = IMAGE.load()
    
    #Get image dimensions, width and length
    dimensions = IMAGE.size

    # A value to keep track of the current RGB value, 0 = R, 1 = G, 2 = B
    currentRGBValue = 0

    # Checks if the image is big enough to contain the given message 
    # The formula for calculating the max. data size to embed is (image width * image height * 3) (because there are 3 RGB values)
    if dimensions[0] * dimensions[1] * 3 > len(arrayOfBits):
    # Nested for loops that iterate through every pixel in the image, starts from top left corner (0,0) to bottom right corner
        for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                for n in range(3):
                    # Grabs the current pixel's RGB values
                    RGB = pixel[i, j]
                    
                    #Checks if theres any Bits left to encode, if not it breaks the loop
                    if len(arrayOfBits) > 0:
                        
                        # Variable to keep track of the current RGB value used, we can only use one at a time R, G, B (Ja jeg er meget god til navngiving)
                        rgb = RGB[currentRGBValue]
                        
                        # Placeholder variables, result is to hold the binary value as a string, the other to hold it as an array
                        result = ''
                        lsb = []

                        # Converts the current RGB value to binary
                        binaryColorValue = bin(rgb)

                        # Goes through every bit in the binary RGB value, and appends it to the lsb array
                        for character in binaryColorValue:
            
                            lsb.append(character)
                        
                        # Logikken under er en del kringlet, forstå så godt som du kan, spørg mig 
                        # Checks if the Current bit we're encoding, matches the last (least significant bit) bit of the RGB value
                        if arrayOfBits[0] != lsb[len(lsb)-1]:
                            # Converts the last bit (saying lsb[-1] takes the last element of the array)-
                            # to an integer so that we may do math to it
                            lsb[-1] = int(lsb[-1])
                            
                            # Adds one so that it matches the bit we're encoding, and takes modulus 2, so that it's always either a 1 or 0 
                            lsb[-1] = (lsb[-1] + 1) % 2

                            # Converts back to string so that we can parse it
                            lsb[-1] = str(lsb[-1])

                        # Converts the lsb array into a string
                        result = ''.join(lsb)

                        # Converts the binary string in result back to an integer
                        k = int(result, 2)

                        # Sets the new R, G or B value to be encoded
                        rgb = k % 256

                        # Removes the current bit so we can take the next
                        arrayOfBits = arrayOfBits[1:]

                        # Changes the RGB value dependent on which RGB value we currently are on (Yes this logic can probably be improved upon)
                        if currentRGBValue == 0:
                            pixel[i, j] = (rgb,RGB[1],RGB[2]) 
                        elif currentRGBValue == 1:
                            pixel[i, j] = (RGB[0],rgb,RGB[2])
                        elif currentRGBValue == 2:
                            pixel[i, j] = (RGB[0],RGB[1],rgb)
                        else:
                            print("Error")
                        
                        # Goes one up in current RGB value, takes modulus 3 so we always stay within 0, 1 or 2
                        currentRGBValue = (currentRGBValue + 1) % 3
                        
                    else:
                        # Saves the image
                        IMAGE.save('C:\Users\theco\OneDrive - Aalborg Universitet\Skrivebord\Uni\1. Semester\Projekter\P1\EncoderDecoder')
                        break
    else:
        print("Your image is too small!")

main()


