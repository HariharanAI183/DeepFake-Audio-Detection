# 🎙️ Fake Voice Detector (Flask Version)

A web app to detect fake (synthetic) voices using deep learning and Flask.

## 🚀 How to Run

1. Clone the project
2. Place your trained model at `model/fake_voice_model.keras`
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python app.py
```

5. Open browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🗂️ Project Structure

- `app.py` - Main Flask app
- `templates/` - HTML UI
- `static/` - CSS styling
- `utils/` - Feature extraction logic
- `uploads/` - Temporary storage for uploaded audio files