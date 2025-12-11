import streamlit as st, tempfile, os
from TTS.api import TTS

@st.cache_resource
def load_tts():
    # 多语言多音色模型，CPU 可跑
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

tts = load_tts()
text = st.text_area("输入文本", "你好，欢迎关注我的 GitHub！")
speaker = st.selectbox("选择音色",
      ["Claribel Dervla", "Damien Black", "Serena Wang", "Xiaoyu 小宇"])  # 16 种内置

if st.button("生成"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tts.tts_to_file(text=text, speaker=speaker, file_path=tmp.name)
        st.audio(tmp.name)
        os.remove(tmp.name)
