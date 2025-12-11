import streamlit as st, requests, tempfile, os

API = "kokoro-onnx-fastapi.railway.internal"
text = st.text_input("文字", "你好世界")
voice = "zh-CN-XiaoxiaoNeural"

if st.button("朗读"):
    try:
        r = requests.post(API, json={"text": text, "voice": voice}, timeout=30)
        # 先别抛异常，把真相打出来
        st.write(f"status_code = {r.status_code}")
        st.write(f"headers = {dict(r.headers)}")
        st.write(f"body = {r.text[:500]}")          # 只看前 500 字符
        r.raise_for_status()                        # 确认无错再往下走
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败：{e}")
        st.stop()

    tmp = tempfile.mktemp(suffix=".mp3")
    with open(tmp, "wb") as f:
        f.write(r.content)
    st.audio(tmp)
    os.remove(tmp)
