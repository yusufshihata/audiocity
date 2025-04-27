import numpy as np

class AudioProcessor:
    def normalize(self, audio: np.ndarray) -> np.ndarray:
        max_amplitude = np.max(np.abs(audio))
        if max_amplitude == 0:
            return audio
        return audio / max_amplitude

    def trim(self, audio: np.ndarray, start: float, end: float, sample_rate: float) -> np.ndarray:
        start_sample = int(start * sample_rate)
        end_sample = int(end * sample_rate)
        if start_sample < 0 or end_sample > len(audio):
            raise ValueError("Invalid time range")
        return audio[start_sample:end_sample]

    def cut_audio(self, audio: np.ndarray, sample_rate: float, start: float, end: float) -> tuple[np.ndarray, np.ndarray]:
        start_sample = int(start * sample_rate)
        end_sample = int(end * sample_rate)

        if start_sample < 0 or end_sample > len(audio) or start_sample > end_sample:
            raise ValueError("Invalid time range")

        segment = audio[start_sample:end_sample]
        remaining = np.concatenate([audio[:start_sample], audio[end_sample:]])
        return segment, remaining

    def copy_audio(self, audio: np.ndarray, sample_rate: float, start: float, end: float) -> tuple[np.ndarray, np.ndarray]:
        start_sample = int(start * sample_rate)
        end_sample = int(end * sample_rate)

        if start_sample < 0 or end_sample > len(audio) or start_sample > end_sample:
            raise ValueError("Invalid time range")

        segment = audio[start_sample:end_sample]
        return segment, audio

    def paste_audio(self, audio: np.ndarray, segment: np.ndarray, sample_rate: float, paste_time: float) -> np.ndarray:
        if sample_rate <= 0:
            raise ValueError("Sample rate must be positive")
        if paste_time < 0:
            raise ValueError("Paste time cannot be negative")

        paste_sample = int(sample_rate * paste_time)

        if paste_sample <= 0:
            return np.concatenate([segment, audio])
        elif paste_sample >= len(audio):
            return np.concatenate([audio, segment])
        else:
            return np.concatenate([
                audio[:paste_sample],
                segment,
                audio[paste_sample:]
            ])

    def delete_audio(self, audio: np.ndarray, sample_rate: float, start: float, end: float) -> np.ndarray:
        _, remaining = self.cut_audio(audio, sample_rate, start, end)
        return remaining
