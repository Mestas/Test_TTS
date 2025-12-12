# tts_player.py
import os, glob, re, time, requests, streamlit as st
from pathlib import Path

# ↓↓↓ 改成你的私有 TTS 接口 ↓↓↓
API_URL = "https://tts-ms-ra-forwarder-production-e395.up.railway.app/api/ra"
VOICE   = "zh-CN-XiaoxiaoNeural"   # 可换 YunxiNeural 等
CHUNK   = 2800                     # 每段最大字数（<3000）

@st.cache_data(show_spinner=False)
def tts_chunk(text: str) -> bytes:
    """调用私有 API，返回 MP3 二进制"""
    payload = {
        "text": text,
        "voice": VOICE,
        "rate": "+0%",
        "volume": "+0%",
        "format": "audio-24khz-48kbitrate-mono-mp3"
    }
    resp = requests.post(API_URL, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.content

def merge_audio(parts: list[bytes]) -> bytes:
    """简单合并 MP3：直接拼二进制即可（Edge-TTS 返回的同为 24 kHz mono）"""
    return b"".join(parts)

def synthesize(long_text: str) -> bytes:
    """超长文本分段合成"""
    if len(long_text) <= CHUNK:
        return tts_chunk(long_text)
    # 按句号分割，避免中途断句
    sentences = re.findall(r'[^。]*.?', long_text)
    buffer, current, parts = "", "", []
    prog = st.progress(0)
    for idx, sent in enumerate(sentences):
        if len(current) + len(sent) <= CHUNK:
            current += sent
        else:
            parts.append(tts_chunk(current))
            current = sent
        prog.progress((idx + 1) / len(sentences))
    if current:
        parts.append(tts_chunk(current))
    prog.empty()
    return merge_audio(parts)

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="文件夹 TTS 播放器", layout="centered")
st.title("📁 私有 TTS 网络播放器")
st.markdown("---")

folder = st.sidebar.text_input("输入github绝对路径", value=str('https://github.com/Mestas/Books/zengguofan3.txt'))
if not os.path.isdir(folder):
    st.sidebar.error("路径无效"); st.stop()

files = sorted(glob.glob(os.path.join(folder, "*.txt")))
if not files:
    st.sidebar.warning("该目录下没有 .txt 文件"); st.stop()

selected = st.sidebar.selectbox("选择要朗读的文本：", files)
st.sidebar.markdown(f"共 `{len(files)}` 个文件")

with open(selected, encoding="utf-8") as f:
    content = f.read()
st.subheader(Path(selected).name)
st.text_area("内容预览：", value=content, height=300)

if st.button("🎙️ 合成语音", type="primary"):
    with st.spinner("正在调用私有 TTS API，请稍候…"):
        start = time.time()
        audio_bytes = synthesize(content)
        cost = time.time() - start
    st.success(f"合成完成！耗时 {cost:.1f} s")
    st.audio(audio_bytes, format="audio/mp3")
    st.download_button(
        label="⬇️ 下载 MP3",
        data=audio_bytes,
        file_name=Path(selected).with_suffix(".mp3").name,
        mime="audio/mp3"
    )
