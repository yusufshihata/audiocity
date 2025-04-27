import numpy as np
from typing import Optional, Union
from abc import ABC, abstractmethod
from engine.src.effects.effect_base import EffectBase


class FadeStrategy(ABC):
    @abstractmethod
    def apply_fade(self, audio, sample_rate: Union[int, float], duration: float, end: Optional[float] = None):
        raise NotImplementedError("Not implemented yet.")

class LinearFadeStrategy(FadeStrategy):
    def apply_fade(self, audio, sample_rate: Union[int, float], duration: float, end: Optional[float] = None):
        if end == None:
            end = audio.shape
        length = int(duration * sample_rate)
        start = end - length

        fade_curve = np.linspace(1.0, 0.0, length)

        audio[start:end] = audio[start:end] * fade_curve

class LogFadeStrategy(FadeStrategy):
    def apply_fade(self, audio, sample_rate: Union[int, float], duration: float, end: Optional[float] = None):
        pass

class FadeEffect(EffectBase):
    def apply(self, audio, sample_rate: Union[int, float], end: Optional[float] = 10.0, duration: Optional[float] = 1.0, fade_strategy: Optional[FadeStrategy] = LinearFadeStrategy):
        return fade_strategy.apply_fade(audio, sample_rate, duration, end)
