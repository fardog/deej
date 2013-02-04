#!/usr/bin/python

from multiprocessing import Process, Value, Lock
import signal

import pyaudio
import numpy
import analyse


def listen(stop, lock):
    """ Listen to the input channel and print the current pitch detected on the input. """
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    MINFREQ = 20.0
    MAXFREQ = 4200.0

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* listening")

    while(True):
        data = stream.read(CHUNK)
        a = numpy.fromstring(data, dtype='int16')
        print (analyse.detect_pitch(a, min_frequency=MINFREQ, max_frequency=MAXFREQ, samplerate=float(RATE)))
        if stop.value > 0:
            lock.acquire()
            break

    print("* done listening")

    stream.stop_stream()
    stream.close()
    p.terminate()
    lock.release()


if __name__ == '__main__':
    stop = Value('i', 0)
    lock = Lock()

    def interrupt_handler(signum, frame):
        stop.value = 1

    signal.signal(signal.SIGINT, interrupt_handler)

    listen_process = Process(target=listen, args=(stop, lock))
    listen_process.start()
    listen_process.join()
