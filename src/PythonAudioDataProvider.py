import pyaudio as pa
import struct




class AudioStream:
    def __init__(self):
        self.CHUNK = 1024 *8
        self.FORMAT = pa.paInt16
        self.CHANNELS = 1
        self.RATE = 44100  # in Hz

        #declare audio stream object
        self.p = pa.PyAudio()
        #open audio stream
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK
        )

    def readData(self):
        data = self.stream.read(self.CHUNK)
        dataInt = struct.unpack(str(self.CHUNK) + 'h', data)
        return dataInt
