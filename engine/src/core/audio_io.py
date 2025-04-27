import librosa
import soundfile as sf
from typing import Optional, Union

def load_audio(file_path: str, sample_rate: Optional[Union[int, float]] = None):
    return librosa.load(file_path, sr=sample_rate)

def save_audio(file_path: str, audio, sample_rate: int):
    try:
        sf.write(file_path, audio, sample_rate)
    except:
        print("Cann't Save the audio file.")
