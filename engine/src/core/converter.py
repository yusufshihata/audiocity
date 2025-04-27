from pydub import AudioSegment

def to_mono(file_path: str):
    sound = AudioSegment.from_wav(file_path)
    sound = sound.set_channels(1)
    sound.export(file_path, format="wav")
    return sound
