"""PyAudio Example: Play a WAVE file."""
import time

import pyaudio
import wave
from tqdm import tqdm


# 播放音频
def play_audio(wave_path):

    CHUNK = 1024

    wf = wave.open(wave_path, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    datas = []
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        datas.append(data)

    for d in tqdm(datas):
        stream.write(d)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


# 回调的方式播放音频，在播放过程中程序可以做其他事情
def play_audio_callback(wave_path):
    CHUNK = 1024

    wf = wave.open(wave_path, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)


    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    # read data
    stream.start_stream()

    while stream.is_active():
        print("1234")
        time.sleep(0.1)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


# 录音
def record_audio(wave_out_path,record_second):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)


    print("* recording")

    for i in tqdm(range(0, int(RATE / CHUNK * record_second))):
        data = stream.read(CHUNK)
        wf.writeframes(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()

    p.terminate()

    wf.close()


if __name__ == '__main__':
    record_audio("output.wav",record_second=4)
    play_audio("output.wav")
