import streamlit as st, edge_tts, tempfile, asyncio, os

voices = [v["Name"] for v in asyncio.run(edge_tts.list_voices()) if "zh-CN" in v["Name"]]
text  = st.text_area("文本", "哈喽，Edge-TTS 在 Streamlit Cloud 上跑得很欢")
voice = st.selectbox("音色", voices)

async def gen():
    tmp = tempfile.mktemp(suffix=".mp3")
    await edge_tts.Communicate(text, voice).save(tmp)
    st.audio(tmp)
    os.remove(tmp)

if st.button("生成"):
    asyncio.run(gen())
