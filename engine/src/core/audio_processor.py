import numpy as np

class AudioProcessor:
    def normalize(self, audio):
        return audio / np.max(np.abs(audio))

    def trim(self, audio, start, end, sample_rate):
        return audio[int(start * sample_rate):int(end * sample_rate)]

