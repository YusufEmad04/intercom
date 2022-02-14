import socket
import threading
import pyaudio

chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 44100

p = pyaudio.PyAudio()

recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True,
                          frames_per_buffer=chunk_size)

playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True,
                        frames_per_buffer=7168)
s = socket.socket()
s.bind(("0.0.0.0", 12344))
s.listen(1)

def r(so):
    while True:
        data = so.recv(7168)
        for i in data:
            print(i)
        playing_stream.write(data)




while True:
    c, addr = s.accept()
    print("got connection from {}".format(addr))

    threading.Thread(target=r, args=(c,)).start()
    while True:
        try:
            x = recording_stream.read(1024)
            c.sendall(x)
        except:
            pass
