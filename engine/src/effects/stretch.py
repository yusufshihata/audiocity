from typing import Union
import librosa
from engine.src.effects.effect_base import EffectBase

class StretchEffect(EffectBase):
    def apply(self, audio, sample_rate: Union[float, int], rate: float):
        if rate < 0:
            raise ValueError("Rate must be postive.")
        return librosa.effects.time_stretch(audio, rate=rate)
