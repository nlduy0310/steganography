from PIL import Image
from utils import *

def change_lsb(value, bit):
    # Convert value to binary
    value = bin(value)
    # Remove the "0b" from the beginning of the string
    value = value[2:]
    # Change the least significant bit to bit
    value = value[:-1] + bit
    value = int(value, 2)
    return value

def lsb_encode(image_path, message):
    # Open the image file
    img = Image.open(image_path)
    # Convert the image to RGB mode
    img = img.convert("RGB")
    # Get the pixel data for the image
    pixels = img.load()

    # convert message to binary
    converted_message = conv2bin(message)
    print(converted_message)
    isPadding = False
    need1bit_padding = False
    
    # check if the message can be encoded in the image
    if img.size[0] * img.size[1] <= len(converted_message):
        print("The message is too long to be encoded in the image!")
        return
    
    # Encode the message in the least significant bits of the pixel values
    for i in range(img.size[0]):
        for j in range(img.size[1]):            
            r, g, b = pixels[i, j]

            if isPadding:
                # padding all other pixels with 0
                r, g, b = pixels[i, j]
                r = change_lsb(r, '0')
                g = change_lsb(g, '0')
                b = change_lsb(b, '0')
                if need1bit_padding:
                    r = change_lsb(r, '1')
                    need1bit_padding = False
                pixels[i, j] = (r, g, b)
                continue

            elif len(converted_message) < 3:
                isPadding = True
                if len(converted_message) == 0:
                    isPadding = True
                    need1bit_padding = True
                    r = change_lsb(r, '0')
                    g = change_lsb(g, '0')
                    b = change_lsb(b, '0')
                elif len(converted_message) == 1:
                    r = change_lsb(r, converted_message[0])
                    g = change_lsb(g, '1')
                    b = change_lsb(b, '0')
                if len(converted_message) == 2:
                    r = change_lsb(r, converted_message[0])
                    g = change_lsb(g, converted_message[1])
                    b = change_lsb(b, '1')
                pixels[i, j] = (r, g, b)
                continue            
            else:
                r = change_lsb(r, converted_message[0])
                g = change_lsb(g, converted_message[1])
                b = change_lsb(b, converted_message[2])
                converted_message = converted_message[3:]
                pixels[i, j] = (r, g, b)
    # Save the steganographic image
    img.save("steganographic_image.png")

def lsb_decode(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Convert the image to RGB mode
    img = img.convert("RGB")
    # Get the pixel data for the image
    pixels = img.load()

    # Decode the message from the least significant bits of the pixel values
    binary = ''
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            binary += bin(r)[-1]
            binary += bin(g)[-1]
            binary += bin(b)[-1]
    
    # calculate the padding to remove
    for i in range(len(binary)-1, -1, -1):
        if binary[i] == '1':
            testbin = binary[:i+20]
            binary = binary[:i]
            break
    # Convert the binary message to a string
    print(binary)
    print(testbin)
    message = bin2str(binary)
    return message

if __name__ == '__main__':
    lsb_encode('lena.png', 'message hidden ehehe :v!!')
    print(lsb_decode("steganographic_image.png"))