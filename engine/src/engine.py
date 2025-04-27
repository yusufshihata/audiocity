from .core.audio_io import load_audio, save_audio
from .core.audio_processor import AudioProcessor
from .core.playback import play_audio
from .effects.fade import FadeEffect
from .effects.stretch import StretchEffect
from .effects.volume import VolumeEffect
from typing import Optional, Tuple
import numpy as np

class AudioEngine:
    def __init__(self):
        self.audio: Optional[np.ndarray] = None
        self.sr: Optional[int] = None
        self.processor = AudioProcessor()
        self.effects = {
            'fade': FadeEffect(),
            'volume': VolumeEffect(),
            'time_stretch': StretchEffect()
        }

    def load(self, file_path: str, sr: Optional[int] = None) -> 'AudioEngine':
        self.audio, self.sr = load_audio(file_path, sr)
        return self

    def load_from_bytes(self, file_content: bytes, sr: Optional[int] = None) -> 'AudioEngine':
        import io
        import librosa
        buffer = io.BytesIO(file_content)
        self.audio, self.sr = librosa.load(buffer, sr=sr)
        return self

    def cut(self, start: float, end: float) -> Tuple[np.ndarray, 'AudioEngine']:
        segment, self.audio = self.processor.cut_audio(self.audio, self.sr, start, end)
        return segment, self

    def copy(self, start: float, end: float) -> np.ndarray:
        segment, _ = self.processor.copy_audio(self.audio, self.sr, start, end)
        return segment

    def paste(self, segment: np.ndarray, paste_time: float) -> 'AudioEngine':
        self.audio = self.processor.paste_audio(self.audio, segment, self.sr, paste_time)
        return self

    def delete(self, start: float, end: float) -> 'AudioEngine':
        self.audio = self.processor.delete_audio(self.audio, self.sr, start, end)
        return self

    def normalize(self):
        self.audio = self.processor.normalize(self.audio)
        return self

    def apply_effect(self, effect_name: str, **kwargs):
        if effect_name not in self.effects:
            raise ValueError(f"Effect '{effect_name}' not found")
        self.audio = self.effects[effect_name].apply(self.audio, self.sr, **kwargs)
        return self

    def play(self):
        if self.audio is not None and self.sr is not None:
            play_audio(self.audio, self.sr)
        else:
            raise ValueError("No audio loaded")
        return self

    def save(self, file_path: str):
        if self.audio is not None and self.sr is not None:
            save_audio(file_path, self.audio, self.sr)
        else:
            raise ValueError("No audio loaded")
        return self

    def save_to_bytes(self):
        if self.audio is None or self.sr is None:
            raise ValueError("No audio loaded")
        import io
        import soundfile as sf
        buffer = io.BytesIO()
        sf.write(buffer, self.audio, self.sr, format='WAV')
        return buffer.getvalue()
