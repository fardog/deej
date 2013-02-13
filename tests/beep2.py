from multiprocessing import Process, Value, Lock
import signal

import pyaudio
import numpy as np
import time
import math
import struct


def main():
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    RATE = 44100.0
    CHANNELS = 2
    FREQUENCY = 440

    constant = 2 * math.pi * FREQUENCY / float(RATE)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    data = [math.sin(i * constant) for i in range(0, CHUNK)]
    wave = struct.pack('f'*len(data), *data)

    while wave != '':
        stream.write(wave)

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    main()