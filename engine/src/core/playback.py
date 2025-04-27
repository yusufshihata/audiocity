import sounddevice as sd

def play_audio(audio, sr):
    sd.play(audio, sr)
    sd.wait()
