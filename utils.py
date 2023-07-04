def conv2bin(message):
    # convert message to binary
    return ''.join(format(ord(i), '08b') for i in message)
def bin2str(binary):
    # convert binary to string
    string = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        string += chr(int(byte, 2))
    return string