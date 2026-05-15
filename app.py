import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
import pyttsx3
import whisper
import tempfile
from audio_recorder_streamlit import audio_recorder

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Voice Translator",
    page_icon="🌍",
    layout="wide"
)

# ---------------- LOAD CSS ----------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🌍 AI Voice Translator")
st.write("🎤 Speak, Translate, and Listen with AI")

# ---------------- TEXT TO SPEECH ----------------
engine = pyttsx3.init()

# ---------------- LANGUAGES ----------------
languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN"
}

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        list(languages.keys())
    )

# ---------------- TEXT INPUT ----------------
text_input = st.text_area("📝 Enter Text")

# ---------------- TRANSLATE TEXT ----------------
if st.button("🌍 Translate Text"):

    if text_input:

        translated = GoogleTranslator(
            source='auto',
            target=languages[target_lang]
        ).translate(text_input)

        st.success("Translation Completed")

        st.subheader("📌 Translated Text")
        st.write(translated)

        # Speak translated text
        engine.say(translated)
        engine.runAndWait()

# ---------------- VOICE INPUT ----------------
st.subheader("🎤 Voice Translation")

if st.button("🎙️ Start Microphone"):

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            st.info("Listening...")

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(
                audio,
                language=languages[source_lang]
            )

            st.subheader("📝 Recognized Text")
            st.write(text)

            translated = GoogleTranslator(
                source='auto',
                target=languages[target_lang]
            ).translate(text)

            st.subheader("🌍 Translated Voice")
            st.write(translated)

            engine.say(translated)
            engine.runAndWait()

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- AUDIO FILE UPLOAD ----------------
st.subheader("📂 Upload Audio File")

uploaded_audio = st.file_uploader(
    "Upload MP3/WAV",
    type=["mp3", "wav"]
)

if uploaded_audio is not None:

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_audio.read())
        temp_audio_path = tmp_file.name

    st.audio(temp_audio_path)

    st.info("Transcribing with Whisper AI...")

    model = whisper.load_model("base")

    result = model.transcribe(temp_audio_path)

    recognized_text = result["text"]

    st.subheader("📝 Whisper Recognized Text")
    st.write(recognized_text)

    translated = GoogleTranslator(
        source='auto',
        target=languages[target_lang]
    ).translate(recognized_text)

    st.subheader("🌍 AI Translation")
    st.write(translated)

# ---------------- HISTORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("💾 Save Translation"):

    if text_input:

        st.session_state.history.append({
            "original": text_input,
            "translated": translated
        })

        st.success("Saved!")

# ---------------- SHOW HISTORY ----------------
st.subheader("📜 Translation History")

for item in st.session_state.history:

    st.write(f"📝 {item['original']}")
    st.write(f"🌍 {item['translated']}")
    st.write("---")