import os

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

def uint2bin(value: int, n_bits=32):
    assert value >= 0
    res = bin(value).removeprefix('0b')
    if n_bits > len(res):
        res = '0' * (n_bits - len(res)) + res
    return res

def bin2uint(binary: str):
    return int(binary, 2)

def get_file_extension(path):
    path = path.strip('.')
    if path.find('.') == -1:
        return None
    else:
        return path.split('.')[-1]
