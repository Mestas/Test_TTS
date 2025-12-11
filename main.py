import streamlit as st, edge_tts, tempfile, asyncio, os

# 1. 选音色
voices = [v["Name"] for v in asyncio.run(edge_tts.list_voices()) if "zh-CN" in v["Name"]]
text  = st.text_area("文本", "哈喽，UA 伪装一下就能过 CDN")
voice = st.selectbox("音色", voices)

# 2. 合成
async def gen():
    tmp = tempfile.mktemp(suffix=".mp3")
    # 关键：加浏览器 UA
    communicate = edge_tts.Communicate(
        text, voice,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
    )
    await communicate.save(tmp)
    st.audio(tmp)
    os.remove(tmp)

if st.button("生成"):
    asyncio.run(gen())
