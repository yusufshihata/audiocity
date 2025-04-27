import numpy as np
import sounddevice as sd

def play_audio(audio, sr):
    sd.play(audio, sr)
    sd.wait()

def cut(audio, sample_rate, start, end):
    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)

    if start_sample < 0 or end_sample > len(audio):
        raise ValueError("Invalid time range.")

    segment = audio[start_sample:end_sample]
    remaining = np.concatenate([audio[:start_sample], audio[end_sample:]])
    return segment, remaining

def copy(audio, sample_rate, start, end):
    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)

    if start_sample < 0 or end_sample > len(audio):
        raise ValueError("Invalid time range.")

    segment = audio[start_sample:end_sample]
    return segment, audio

def paste(audio, segment, sample_rate, paste_time):
    paste_sample = int(sample_rate * paste_time)

    if paste_sample <= 0:
        return np.concatenate([segment, audio])
    elif paste_sample > len(audio):
        return np.concatenate([audio, segment])
    else:
        return np.concatenate(audio[paste_sample:], segment, audio[:paste_sample])

def delete(audio, sample_rate, start, end):
    _, remaining = cut(audio, sample_rate, start, end)

    return remaining

