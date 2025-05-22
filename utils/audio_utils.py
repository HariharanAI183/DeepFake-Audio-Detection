import librosa
import numpy as np

def extract_features(file_path, sr=16000, n_mfcc=13, max_len=100):
    y, _ = librosa.load(file_path, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc = librosa.util.fix_length(mfcc, size=max_len, axis=1)
    return mfcc.T