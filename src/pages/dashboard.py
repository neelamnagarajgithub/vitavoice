import streamlit as st
import numpy as np
from services.engine import queries
from services.murfservice import stream_tts_to_bytes, translate_texts_to_buffer
from services.whisper_stt import speech_to_text, store_audio_in_mongo
from pymongo import MongoClient
import os
import io

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

    # Record audio input with Streamlit
    st.markdown("##### Or record your message:")
    audio_file = st.audio_input("Record your voice")

    if audio_file is not None:
        with st.spinner("Transcribing..."):
            audio_bytes = audio_file.getvalue()
            buf = io.BytesIO(audio_bytes)

            # Store audio in MongoDB
            audio_id = store_audio_in_mongo(st.session_state.username, buf)

            # Run Whisper STT
            recognized = speech_to_text(audio_id)
            st.session_state.recognized_text = recognized

        st.success("Transcription complete!")
        st.rerun()

    # Send message (typed or transcribed)
    if st.button("Send"):
        query_text = st.session_state.recognized_text or user_query.strip()
        if query_text:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "text": query_text})
            save_message(st.session_state.username, "user", query_text)

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