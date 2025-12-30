# st_test_tts.py
import streamlit as st, requests, time, pathlib, io

# ========== 配置 ==========
API_URL = "RcTDoGnhP4O0ZqQbUiqoI0vS"  # ← 你的私有地址
VOICE   = "female_chinese"
MAX_CHUNK = 2000   # 单段上限（Edge-TTS 建议 <3k）

# ========== 逻辑 ==========
@st.cache_data(show_spinner=False)
def tts_chunk(text: str) -> bytes:
    payload = dict(
        text=text,
        voice=VOICE,
        rate="+0%",
        volume="+0%",
        format="audio-24khz-48kbitrate-mono-mp3",
    )
    resp = requests.post(API_URL, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.content

def synthesize(long_text: str) -> bytes:
    if len(long_text) <= MAX_CHUNK:
        return tts_chunk(long_text)
    # 按句号分段
    parts, para = [], ""
    for s in long_text.split("。"):
        if len(para + s) <= MAX_CHUNK:
            para += s + "。"
        else:
            parts.append(tts_chunk(para))
            para = s + "。"
    if para:
        parts.append(tts_chunk(para))
    return b"".join(parts)

# ========== UI ==========
st.set_page_config(page_title="TTS 手写测试", layout="centered")
st.title("✍️ 手写文字 · TTS 测试播放器")
st.markdown("---")

with st.form("form"):
    text = st.text_area("请输入要合成的文字（支持回车换行）：", height=120,
                        value="你好，这是一条手写测试，能听到就说明私有 TTS API 正常工作！")
    submitted = st.form_submit_button("🎙️ 合成并播放", type="primary")

if submitted:
    if not text.strip():
        st.warning("文字不能为空"); st.stop()
    with st.spinner("正在调用私有 TTS API …"):
        t0 = time.time()
        try:
            audio_bytes = synthesize(text.strip())
        except Exception as e:
            st.error(f"❌ 合成失败：{e}"); st.stop()
    st.success(f"✅ 合成完成！耗时 {time.time()-t0:.1f}s")
    st.audio(audio_bytes, format="audio/mp3")
    st.download_button(
        label="⬇️ 下载 MP3",
        data=audio_bytes,
        file_name=f"tts_{int(time.time())}.mp3",
        mime="audio/mp3"
    )
