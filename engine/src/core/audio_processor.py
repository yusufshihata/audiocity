import numpy as np

class AudioProcessor:
    def normalize(self, audio):
        return audio / np.max(np.abs(audio))

    def trim(self, audio, start, end, sr):
        return audio[int(start * sr):int(end * sr)]
