# DeepFake Audio Detection Web App

A Flask-based web app that allows users to record or upload an audio file and classifies it as **real or fake** using a deep learning model trained on MFCC features.

---

##  Features

-  Record voice using browser microphone
-  Upload audio (WAV or MP3)
-  Real-time prediction (DeepFake vs Real)
-  MFCC-based audio preprocessing
-  TensorFlow-based model for inference

---

##  Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Audio Processing:** `pydub`, `scipy`, `python_speech_features`
- **Model Framework:** TensorFlow
- **Deployment-ready** for Hugging Face Spaces, Render, or any Flask-compatible service

---

##  Setup Instructions

```bash
# Clone the repository
git clone https://github.com/HariharanAI183/DeepFake-Audio-Detection.git
cd DeepFake-Audio-Detection

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py



├── app.py                      # Flask app
├── model/
│   └── fake_voice_model.pkl    # Trained model
├── static/
│   ├── style.css               # Styling
│   └── script.js               # JS if used
├── templates/
│   └── index.html              # HTML UI
├── utils/
│   └── audio_utils.py          # Audio processing functions
├── ffmpeg/                     # Optional FFmpeg binary if needed
├── requirements.txt            # Dependencies
└── README.md                   # This file

```
