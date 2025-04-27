from typing import Union
from abc import ABC, abstractmethod

class EffectBase(ABC):
    @abstractmethod
    def apply(self, audio, sample_rate: Union[int, float], **kwargs):
        raise NotImplementedError("This function is not implemented here")
