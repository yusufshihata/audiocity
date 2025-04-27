from engine.src.effects.effect_base import EffectBase

class VolumeEffect(EffectBase):
    def apply(self, audio, sample_rate, gain=1.0):
        return audio * gain

