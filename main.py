from engine.src.core.audio_io import load_audio, save_audio
from engine.src.core.playback import play_audio

audio, sr = load_audio('new_audio.wav')

play_audio(audio, sr)

