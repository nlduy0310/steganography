from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
from utils import *
from core import change_lsb

class AudioSteg:
    def wav_data(wav_file):
        sample_rate, data = wavfile.read(wav_file)
        return sample_rate, data, data.shape[0], data.shape[1]
    
    def save_wav(sample_rate, data, filename):
        wavfile.write(filename, sample_rate, data)
    
    class LSB:
        ReservedBits = 32
        AllChannels = [-1]

        def check_message_size(data, message, is_bin=False):                
            message_len = len(message)
            if not is_bin:
                message_len *= 8

            if message_len >= data.shape[0] - AudioSteg.LSB.ReservedBits:
                return False
            
            return True


        def encode(data, message, channels=AllChannels):
            if not AudioSteg.LSB.check_message_size(data, message):
                return False, f'Message size ({len(message)}) exceeds file limit ({(data.shape[0] - AudioSteg.LSB.ReservedBits) // 8})'
            
            bin_message = conv2bin(message)
            
            if channels == AudioSteg.LSB.AllChannels:
                channels = list(range(0, data.shape[1]))

            for channel in channels:
                if channel >= 0 and channel < data.shape[1]:
                    AudioSteg.LSB.__encode_channel(data[:, channel], bin_message)

            return True, 'Message has been encoded into your file'

        def __set_reserved_bits(channel_data, bin):
            for i in range(AudioSteg.LSB.ReservedBits):
                sign = 1 if channel_data[i] >= 0 else -1
                channel_data[i] = sign * change_lsb(sign * channel_data[i], bin[i])
            return channel_data

        def __encode_channel(channel_data, bin_message):
            reserved_bits = uint2bin(len(bin_message))
            channel_data = AudioSteg.LSB.__set_reserved_bits(channel_data, reserved_bits)

            for i in range(len(bin_message)):
                sign = 1 if channel_data[AudioSteg.LSB.ReservedBits + i] >= 0 else -1
                channel_data[AudioSteg.LSB.ReservedBits + i] = sign * change_lsb(sign * channel_data[AudioSteg.LSB.ReservedBits + i], bin_message[i])
            
        def decode(data, channels=AllChannels):
            res = []

            if channels == AudioSteg.LSB.AllChannels:
                channels = list(range(0, data.shape[1]))
            
            for channel in channels:
                if channel >= 0 and channel < data.shape[1]:
                    res.append(AudioSteg.LSB.__decode_channel(data[:, channel]))

            return res

        def __get_reserved_bits(channel_data):
            res = ''
            for i in range(AudioSteg.LSB.ReservedBits):
                sign = 1 if channel_data[i] >= 0 else -1
                res += uint2bin(sign * channel_data[i])[-1]
            return res

        def __decode_channel(channel_data):
            reserved_bits = AudioSteg.LSB.__get_reserved_bits(channel_data)
            message_bits = bin2uint(reserved_bits)

            bin_message = ''
            for i in range(message_bits):
                sign = 1 if channel_data[AudioSteg.LSB.ReservedBits + i] >= 0 else -1
                bin_message += uint2bin(sign * channel_data[AudioSteg.LSB.ReservedBits + i])[-1]

            return bin2str(bin_message)

if __name__ == '__main__':
    # read
    sample_rate, original_data, n_samples, n_channels = AudioSteg.wav_data('sample.wav')
    edited_data = original_data.copy()

    # encode
    AudioSteg.LSB.encode(edited_data, 'Hello World', channels=[0])
    AudioSteg.LSB.encode(edited_data, 'Lorem ipsum..@!$@', channels=[1])
    AudioSteg.save_wav(sample_rate, edited_data, 'sample_with_message.wav')

    # decode
    sample_rate, data, _, __ = AudioSteg.wav_data('sample_with_message.wav')
    res0 = AudioSteg.LSB.decode(data, channels=[0])
    res1 = AudioSteg.LSB.decode(data, channels=[1])
    print(f'Decoded message: {res0}, {res1}')
