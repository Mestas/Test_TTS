import requests, streamlit as st
# API = "https://tts-kokoro-onnx-fastapi.up.railway.app/generate-speech"
API = "https://kokoro-onnx-fastapi-production.up.railway.app"
text = st.text_input("文字", "你好，私有 TTS")
if st.button("合成"):
    r = requests.post(API, json={"text": text, "voice": "zf_001", "speed": 1.0})
    st.audio(r.content, format="audio/wav")
