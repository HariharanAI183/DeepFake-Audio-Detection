import numpy as np
import io
import scipy.io.wavfile as wav
import tensorflow as tf
from python_speech_features import mfcc
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    model = tf.keras.models.load_model("model/fake_voice_model.keras")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

LABELS = ['Fake', 'Real']

def preprocess_audio(audio_bytes, max_len=100):
    try:
        # Read audio bytes as WAV format using scipy
        sample_rate, signal = wav.read(io.BytesIO(audio_bytes))
        
        # Convert stereo to mono if needed
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)
            
        # Normalize audio signal
        signal = signal / np.max(np.abs(signal))
        
        # Extract MFCC features
        features = mfcc(
            signal,
            samplerate=sample_rate,
            numcep=13,
            nfilt=26,
            nfft=2048,
            winlen=0.025,
            winstep=0.01
        )

        # Padding or truncating to max_len
        if features.shape[0] < max_len:
            pad_width = max_len - features.shape[0]
            features = np.pad(features, ((0, pad_width), mode=='constant'))
        else:
            features = features[:max_len]

        return features[np.newaxis, ..., np.newaxis]
    except Exception as e:
        logger.error(f"Audio processing error: {e}")
        raise RuntimeError(f"Failed to process audio: {e}")

def predict_fake_or_real(mfcc):
    try:
        prediction = model.predict(mfcc)[0]
        predicted_class = int(round(prediction[0]))
        label = LABELS[predicted_class]
        confidence = float(prediction[0]) if label == 'Real' else 1 - float(prediction[0])
        confidence = max(0.0, min(1.0, confidence))  # Ensure confidence is between 0 and 1
        return label, round(confidence, 2)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise RuntimeError(f"Failed to make prediction: {e}")