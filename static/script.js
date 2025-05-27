let mediaRecorder;
let audioChunks = [];
let audioBlob;
let mediaStream;
let currentObjectURL;

window.onload = () => {
  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");
  const predictBtn = document.getElementById("predictBtn");
  const uploadBtn = document.getElementById("uploadBtn");
  const fileInput = document.getElementById("fileInput");
  const audioPlayer = document.getElementById("audioPlayer");
  const uploadedPlayer = document.getElementById("uploadedPlayer");
  const resultText = document.getElementById("result");

  const setResult = (text, color="black") => {
    resultText.textContent = text;
    resultText.style.color = color;
  };

  const cleanupMedia = () => {
    if (mediaStream) {
      console.log("mediaStream:", mediaStream);
      mediaStream.getTracks().forEach(track => track.stop());
      mediaStream = null;
    }
  };

  const revokeURL = () => {
    if (currentObjectURL) {
      URL.revokeObjectURL(currentObjectURL);
      currentObjectURL = null;
    }
  };

  

  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) {
      document.getElementById("fileName").textContent = fileInput.files[0].name;
      revokeURL();
      currentObjectURL = URL.createObjectURL(fileInput.files[0]);
      uploadedPlayer.src = currentObjectURL;
    }
  });

  startBtn.onclick = async () => {
    try {
      cleanupMedia();
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStream = stream;
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) audioChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        revokeURL();
        currentObjectURL = URL.createObjectURL(audioBlob);
        audioPlayer.src = currentObjectURL;
        predictBtn.disabled = false;
      };

      mediaRecorder.start(100);
      startBtn.disabled = true;
      stopBtn.disabled = false;
      predictBtn.disabled = true;
      setResult("");
    } catch (err) {
      console.error("Error accessing mic:", err);
      setResult("Error: Could not access microphone. Check permissions.", "red");
    }
  };

  stopBtn.onclick = () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
      cleanupMedia();
      stopBtn.disabled = true;
      startBtn.disabled = false;
    }
  };

  const predictAudio = async (blob, isUploaded=false) => {
    setResult("Processing...", "blue");

    const formData = new FormData();
    formData.append("audio", blob, isUploaded ? "uploaded.wav" : "recorded.wav");

    try {
      const response = await fetch("/upload", { method: "POST", body: formData });
      const data = await response.json();

      if (!response.ok) throw new Error(data.error || "Server error");
      const color = data.label === "Real" ? "green" : "red";
      setResult(`Prediction: ${data.label} (Confidence: ${data.confidence})`, color);
    } catch (err) {
      console.error("Error:", err);
      let msg = err.message;
      if (msg.match(/FFmpeg|convert/)) msg += " — please try uploading a WAV file.";
      setResult(`Error: ${msg}`, "red");
    }
  };

  predictBtn.onclick = () => {
    if (audioBlob) predictAudio(audioBlob);
  };

  uploadBtn.onclick = () => {
    if (!fileInput.files[0]) {
      setResult("Please select an audio file first", "red");
      return;
    }
    const file = fileInput.files[0];
    if (!file.type.startsWith("audio/")) {
      setResult("Selected file is not audio", "red");
      return;
    }
    predictAudio(file, true);
  };

  window.addEventListener("beforeunload", cleanupMedia);
};
