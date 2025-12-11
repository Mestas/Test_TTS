import requests
API = "https://tts-kokoro-onnx-fastapi.up.railway.app"
payload = {"text": "你好，私有 TTS！", "voice": "zf_001", "speed": 1.0}
r = requests.post(API, json=payload)
with open("output.wav", "wb") as f:
    f.write(r.content)
