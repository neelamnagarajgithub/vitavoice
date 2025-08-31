import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import numpy as np
from services.engine import queries
from services.murfservice import stream_tts_to_bytes, translate_texts_to_buffer
from services.whisper_stt import speech_to_text
from pymongo import MongoClient
import os
import soundfile as sf
import io

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        pcm = frame.to_ndarray().flatten()
        self.audio_frames.append(pcm)
        return frame

# MongoDB setup (move this to a config or service file if you prefer)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vitavoice"]
chats_col = db["chats"]

def save_message(username, role, text, audio_bytes=None):
    doc = {
        "username": username,
        "role": role,
        "text": text,
        "audio": audio_bytes.getvalue() if audio_bytes else None
    }
    chats_col.insert_one(doc)

def load_chat_history(username):
    chat_history = []
    for doc in chats_col.find({"username": username}):
        entry = {
            "role": doc["role"],
            "text": doc["text"]
        }
        if doc["role"] == "ai" and doc.get("audio"):
            from io import BytesIO
            entry["audio"] = BytesIO(doc["audio"])
        chat_history.append(entry)
    return chat_history

def save_mic_audio_locally(audio_frames, filename="mic_input.wav"):
    if audio_frames:
        audio_np = np.concatenate(audio_frames).astype(np.int16)
        sf.write(filename, audio_np, 16000, format="WAV")
        return filename
    return None

def app():
    st.title("AI Doctor Chat")
    st.success(f"Welcome, {st.session_state.username}!")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    languages = {
        "English": "en-UK-ruby",
        "Hindi": "hi-IN-ayushi",
        "Spanish": "es-MX-valeria",
        "French": "fr-FR-adélie",
        "German": "de-DE-matthias"
    }
    languages_translation = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Spanish": "es-MX",
        "French": "fr-FR",
        "German": "de-DE"
    }
    selected_language = st.selectbox("Select language for response", list(languages.keys()), key="lang_select")

    st.markdown("#### Chat with your AI Doctor:")

    # Display chat history
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(
                "<div style='background:#e6f7ff;padding:8px;border-radius:8px;margin-bottom:4px;color:#222;font-weight:500;'>"
                "<b>You:</b> {}</div>".format(entry['text']),
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='background:#f6ffed;padding:8px;border-radius:8px;margin-bottom:4px;color:#174317;font-weight:500;'>"
                "<b>AI Doctor:</b> {}</div>".format(entry['text']),
                unsafe_allow_html=True
            )
            st.audio(entry["audio"], format="audio/wav")

    # --- Input area ---
    if "recognized_text" not in st.session_state:
        st.session_state.recognized_text = ""

    user_query = st.text_input(
        "Type your message",
        value=st.session_state.recognized_text,
        key="user_query"
    )

    # Record button below text field
    st.markdown("##### Or record your message:")
    ctx = webrtc_streamer(
        key="speech",
        audio_receiver_size=4096,
        media_stream_constraints={"audio": True, "video": False},
        audio_processor_factory=AudioProcessor,
        async_processing=False,
    )
    if "mic_audio_frames" not in st.session_state:
        st.session_state.mic_audio_frames = []

    # Clear buffer before new recording
    if st.button("START"):
        st.session_state.mic_audio_frames = []
        st.session_state.mic_audio_saved = False
        st.session_state.mic_audio_path = None

    if ctx.audio_processor is not None and hasattr(ctx.audio_processor, "audio_frames"):
        st.session_state.mic_audio_frames = ctx.audio_processor.audio_frames

        # Save audio when recording stops (i.e., when there are frames and not already saved)
        if st.session_state.mic_audio_frames and not st.session_state.get("mic_audio_saved", False):
            audio_path = save_mic_audio_locally(st.session_state.mic_audio_frames, f"{st.session_state.username}_mic_input.wav")
            st.session_state.mic_audio_saved = True
            st.session_state.mic_audio_path = audio_path

    if st.button("Transcribe Mic Input"):
        audio_path = st.session_state.get("mic_audio_path")
        if audio_path and os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                buf = io.BytesIO(f.read())
            # Store audio in MongoDB and get audio_id
            from services.whisper_stt import store_audio_in_mongo, speech_to_text
            audio_id = store_audio_in_mongo(st.session_state.username, buf)

            with st.spinner("Transcribing..."):
                recognized = speech_to_text(audio_id)
                st.session_state.recognized_text = recognized

            st.success("Transcription complete!")
            st.rerun()
        else:
            st.warning("No audio file found. Please record and try again.")

    # Send message (typed or transcribed)
    if st.button("Send"):
        query_text = st.session_state.recognized_text or user_query.strip()
        if query_text:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "text": query_text})

            # Get AI response and TTS audio
            result = queries(st.session_state.username, query_text)
            if languages_translation[selected_language] != "en-IN":
                response = translate_texts_to_buffer([str(result)], target_language=languages_translation[selected_language])
                translated_text = response.translations[0].translated_text
            else:
                translated_text = str(result)
            audio_bytes = stream_tts_to_bytes(translated_text, voice_id=languages[selected_language])

            # Add AI message to chat history
            st.session_state.chat_history.append({
                "role": "ai",
                "text": translated_text,
                "audio": audio_bytes
            })

            # Save the message to MongoDB
            save_message(st.session_state.username, "ai", translated_text, audio_bytes)

            st.session_state.recognized_text = ""
            st.rerun()
        else:
            st.warning("Please type or record a message.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.chat_history = []
        st.rerun()
