from engine.src.core.audio_io import load_audio, save_audio
from engine.src.core.playback import play_audio
from engine.src.core.audio_processor import AudioProcessor

audio, sr = load_audio('new_audio.wav')


processor = AudioProcessor()

audio = processor.normalize(audio)

audio = processor.trim(audio, 0, 5, sr)

play_audio(audio, sr)

