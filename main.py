from engine.src.core.audio_io import load_audio, save_audio
from engine.src.core.playback import play_audio, cut, delete, paste, copy
from engine.src.core.audio_processor import AudioProcessor

audio, sr = load_audio('wag_dog_plan.wav')

segment, audio = copy(audio, sr, 3, 4)

audio = paste(audio, segment, sr, 0)

audio = delete(audio, sr, 0, 4)

play_audio(audio, sr)

