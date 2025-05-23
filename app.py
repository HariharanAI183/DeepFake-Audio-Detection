import os
import subprocess
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin', 'ffmpeg.exe')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'message': 'No audio file part'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed'}), 400

    # Initialize paths as None
    input_path = None
    output_path = None

    try:
        # Save original file
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Convert to WAV
        output_path = os.path.join(UPLOAD_FOLDER, 'converted.wav')
        
        # Using system FFmpeg (since it's in PATH)
        result = subprocess.run([
            'ffmpeg', '-y', '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            output_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")

        # Read converted file
        with open(output_path, 'rb') as f:
            audio_bytes = f.read()

        # Process audio (replace with your actual processing)
        # mfcc = preprocess_audio(audio_bytes)
        # label, confidence = predict_fake_or_real(mfcc)
        
        # For testing, return dummy values
        label = "Real"
        confidence = 0.95

        return jsonify({
            'label': label,
            'confidence': confidence
        })

    except Exception as e:
        # Clean up if files exist (now using the initialized variables)
        if input_path and os.path.exists(input_path):
            os.remove(input_path)
        if output_path and os.path.exists(output_path):
            os.remove(output_path)
            
        return jsonify({'message': f'Processing error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)