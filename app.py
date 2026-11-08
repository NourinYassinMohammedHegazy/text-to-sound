import streamlit as st
import edge_tts
import asyncio
import io
 
st.title(" حول النص إلى صوت!")
 
text = st.text_area("اكتب النص هنا:")
 
lang = st.selectbox("اختار اللغة:", ["عربي", "إنجليزي"])
 
VOICES = {
    "عربي": {
        
        " زارية (امرأة - السعودية)": "ar-SA-ZariyahNeural",
        " جمال (رجل - مصر)":         "ar-EG-ShakirNeural",
        " سلمى (امرأة - مصر)":       "ar-EG-SalmaNeural",
    },
    "إنجليزي": {
        " غاي (رجل - أمريكا)":       "en-US-GuyNeural",
        " جيني (امرأة - أمريكا)":    "en-US-JennyNeural",
        " رايان (رجل - بريطانيا)":   "en-GB-RyanNeural",
        " ليبرا (امرأة - بريطانيا)": "en-GB-LibbyNeural",
    },
}
 
voice_label = st.selectbox("اختار الصوت:", list(VOICES[lang].keys()))
voice_id = VOICES[lang][voice_label]
 
async def generate_audio(text, voice):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    return b"".join(audio_chunks)
 
if st.button("تشغيل الصوت"):
    if text:
        audio_bytes = asyncio.run(generate_audio(text, voice_id))
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("اكتب نص أولاً! ")
