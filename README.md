```markdown
# Fake Voice Detection Web App

A Flask web app that allows users to either record audio directly from the browser or upload a file, and it classifies the audio as real or fake using a trained deep learning model.

## Features
- Record voice using browser microphone
- Upload pre-recorded audio
- Real-time predictions
- MFCC feature extraction

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Folder Structure
```
├── app.py
├── model/
│   └── fake_voice_model.keras
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── utils/
│   └── audio_utils.py
├── test_audio/
├── requirements.txt
└── README.md
```
```