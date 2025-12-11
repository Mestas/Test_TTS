import streamlit as st, tempfile, os
from TTS.api import TTS

@st.cache_resource
def load():
    return TTS("tts_models/zh-CN/baker/tacotron2-DDC")

tts = load()
text = st.text_area("文本", "离线模型再也不怕 CDN 阻断")
if st.button("生成"):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tts.tts_to_file(text=text, file_path=f.name)
        st.audio(f.name)
        os.remove(f.name)
