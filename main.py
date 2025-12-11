# app.py
import streamlit as st, tempfile, os
from TTS.api import TTS

@st.cache_resource(show_spinner="正在加载模型…")
def load():
    # 确认存在的模型名
    return TTS("tts_models/zh-CN/baker/tacotron2-DDC-ph")

tts = load()
text = st.text_area("输入中文", "今天天气真不错")
if st.button("生成"):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tts.tts_to_file(text=text, file_path=f.name)
        st.audio(f.name)
        os.remove(f.name)
