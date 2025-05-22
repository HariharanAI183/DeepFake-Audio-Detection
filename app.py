from flask import Flask, render_template, request, redirect, url_for
import os
import tensorflow as tf
import numpy as np
from utils.audio_utils import extract_features
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load model
model = tf.keras.models.load_model("model/fake_voice_model.keras")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files['audio_file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            features = extract_features(file_path)
            features = np.expand_dims(features, axis=0)
            prediction = model.predict(features)[0]

            label = "Real Voice" if prediction[0] < 0.5 else "Fake Voice"
            confidence = prediction[0] if label == "Fake Voice" else 1 - prediction[0]

            result = f"{label} (Confidence: {confidence:.2f})"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)