import requests, tempfile, os, streamlit as st

API = "https://edge-tts.vercel.app/api"
text = st.text_input("文字", "你好世界")
voice = "zh-CN-XiaoxiaoNeural"

if st.button("朗读"):
    r = requests.post(API, json={"text": text, "voice": voice}, timeout=30)
    r.raise_for_status()
    tmp = tempfile.mktemp(suffix=".mp3")
    with open(tmp, "wb") as f:
        f.write(r.content)
    st.audio(tmp)
    os.remove(tmp)
