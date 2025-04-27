import numpy
from typing import Optional, Union
from abc import ABC, abstractmethod
from effects.effect_base import EffectBase


class FadeStrategy(ABC):
    @abstractmethod
    def apply_fade(self, audio, sample_rate: Union[int, float], duration: float):
        raise NotImplementedError("Not implemented yet.")

class LinearFadeStrategy(FadeStrategy):
    def apply_fade(self, audio, sample_rate: Union[int, float], duration: float):
        pass

class LogFadeStrategy(FadeStrategy):
    def apply_fade(self, audio, sample_rate: Union[int, float], duration: float):
        pass

class FadeEffect(EffectBase):
    def apply(self, audio, sample_rate: Union[int, float], duration: Optional[float] = 1.0, fade_type: Optional[FadeStrategy] = LinearFadeStrategy):
        # TODO: Apply the fade effect in audio here
        pass

