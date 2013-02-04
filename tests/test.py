#!/usr/bin/python

from multiprocessing import Process, Value, Lock
import pyaudio
import wave
import numpy
import time
import analyse


def record(stop, lock):

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    WAVE_OUTPUT_FILENAME = 'output.wav'

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    while(True):
        data = stream.read(CHUNK)
        a = numpy.fromstring(data, dtype='int16')
        print (analyse.detect_pitch(a, min_frequency=60.0, max_frequency=1500.0))
        # print (numpy.abs(a).mean())
        wf.writeframes(data)
        if stop.value > 0:
            lock.acquire()
            break

    print("* done recording")

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()
    lock.release()


if __name__ == '__main__':
    stop = Value('i', 0)
    lock = Lock()

    record_process = Process(target=record, args=(stop, lock))
    record_process.start()

    time.sleep(100)
    stop.value = 1
    time.sleep(1)

    record_process.join()
    print("* record threads finished, quitting")
