let mediaRecorder;
let audioChunks = [];
let audioBlob;
let mediaStream;

window.onload = () => {
  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");
  const predictBtn = document.getElementById("predictBtn");
  const uploadBtn = document.getElementById("uploadBtn");
  const fileInput = document.getElementById("fileInput");
  const audioPlayer = document.getElementById("audioPlayer");
  const uploadedPlayer = document.getElementById("uploadedPlayer");
  const resultText = document.getElementById("result");

  const cleanupMedia = () => {
    if (mediaStream) {
      mediaStream.getTracks().forEach(track => track.stop());
      mediaStream = null;
    }
  };

  // Add this to your window.onload function
  fileInput.onchange = () => {
    if (fileInput.files && fileInput.files[0]) {
      document.getElementById("fileName").textContent = fileInput.files[0].name;
      const audioUrl = URL.createObjectURL(fileInput.files[0]);
      uploadedPlayer.src = audioUrl;
    }
  };

  startBtn.onclick = async () => {
    try {
      cleanupMedia();
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStream = stream;

      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayer.src = audioUrl;
        predictBtn.disabled = false;
      };

      mediaRecorder.start(100); // Collect data every 100ms
      startBtn.disabled = true;
      stopBtn.disabled = false;
      predictBtn.disabled = true;
      resultText.textContent = "";
    } catch (err) {
      console.error("Error accessing microphone:", err);
      resultText.textContent = "Error: Could not access microphone. Please check permissions.";
    }
  };

  stopBtn.onclick = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      cleanupMedia();
      stopBtn.disabled = true;
      startBtn.disabled = false;
    }
  };

  const predictAudio = async (blob, isUploaded = false) => {
    const resultText = document.getElementById("result");
    resultText.textContent = "Processing...";
    resultText.style.color = "blue";

    const formData = new FormData();
    formData.append('audio', blob, isUploaded ? 'uploaded.wav' : 'recorded.wav');

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Server processing failed');
        }

        resultText.textContent = `Prediction: ${data.label} (Confidence: ${data.confidence})`;
        resultText.style.color = data.label === 'Real' ? "green" : "red";
    } catch (err) {
        console.error("Error:", err);
        resultText.textContent = `Error: ${err.message}`;
        resultText.style.color = "red";
        
        // Special handling for FFmpeg errors
        if (err.message.includes('FFmpeg') || err.message.includes('convert')) {
            resultText.textContent += ". Please try uploading a WAV file.";
        }
    }
  };
  predictBtn.onclick = async () => {
    if (audioBlob) {
      await predictAudio(audioBlob);
    }
  };

  uploadBtn.onclick = async () => {
    if (!fileInput.files || !fileInput.files[0]) {
      resultText.textContent = "Please select an audio file first";
      return;
    }

    const file = fileInput.files[0];
    if (!file.type.includes('audio/')) {
      resultText.textContent = "Please select an audio file";
      return;
    }

    const audioUrl = URL.createObjectURL(file);
    uploadedPlayer.src = audioUrl;

    try {
      await predictAudio(file, true);
    } catch (err) {
      console.error("Upload error:", err);
      resultText.textContent = `Error: ${err.message}`;
    }
  };

  // Cleanup on page unload
  window.addEventListener('beforeunload', cleanupMedia);
};