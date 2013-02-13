import pyaudio


def beep():
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    RATE = 44100
    CHANNELS = 2
    FREQUENCY = 440

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    count = 0
    while True:
        beep = chr(63) + chr(63) + chr(63) + chr(63)
        stream.write(beep)
        beep = chr(0) + chr(0) + chr(0) + chr(0)
        stream.write(beep)
        count = count + 1

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    beep()
