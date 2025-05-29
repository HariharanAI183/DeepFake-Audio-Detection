import io
import os
import subprocess
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from utils.audio_utils import preprocess_audio, predict_fake_or_real
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
ALLOWED_EXT = {'wav', 'mp3', 'ogg', 'm4a'}
AudioSegment.converter = os.path.join(app.root_path, 'ffmpeg', 'bin', 'ffmpeg.exe')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def convert_webm_to_wav_bytes(webm_bytes):
    process = subprocess.run(
        [
            'ffmpeg',
            '-i', 'pipe:0',         
            '-f', 'wav',            
            '-ar', '16000',         
            '-ac', '1',             
            'pipe:1'                
        ],
        input=webm_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {process.stderr.decode()}")

    return io.BytesIO(process.stdout)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify(error='No audio file uploaded'), 400

    file = request.files['audio']
    if not file or file.filename == '':
        return jsonify(error='No file selected'), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()

    if ext not in ALLOWED_EXT:
        return jsonify(error=f'Unsupported file type .{ext}'), 400

    audio_bytes = file.read()
    audio_bytes = convert_webm_to_wav_bytes(audio_bytes)
    if not audio_bytes:
        return jsonify(error='Uploaded file is empty'), 400

    if ext != 'wav':
        try:
            audio_bytes = AudioSegment.from_file(io.BytesIO(audio_bytes), format=ext)\
                                     .export(format='wav').read()
        except Exception as e:
            app.logger.error(f"Conversion failed: {e}")
            return jsonify(error='Could not convert to WAV'), 400

    try:
        mfcc = preprocess_audio(audio_bytes.getvalue())
        label, confidence = predict_fake_or_real(mfcc)
    except Exception as e:
        app.logger.error(f"Processing failed: {e}")
        return jsonify(error='Audio processing error'), 500

    return jsonify(label=label, confidence=confidence)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)