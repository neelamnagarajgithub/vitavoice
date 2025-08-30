import json
import streamlit as st
from services.engine import queries
from services.murfservice import stream_tts_to_bytes, translate_texts_to_buffer

def app():
    st.title("Dashboard")
    st.success(f"Welcome, {st.session_state.username}!")
    
    user_query = st.text_input("Enter your query:", key="user_query")
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

    if st.button("Submit Query"):
        if user_query.strip():
            result = queries(st.session_state.username, user_query)
            # Translate result if not English
            if languages_translation[selected_language] != "en-IN":
                buffer = translate_texts_to_buffer([str(result)], target_language=languages_translation[selected_language])
                translation_json = buffer.read().decode("utf-8")
                translation_data = json.loads(translation_json)
                # Get all translated_texts and join them
                translated_text = " ".join([t["translated_text"] for t in translation_data["translations"]])
            else:
                translated_text = str(result)
            audio_bytes = stream_tts_to_bytes(translated_text, voice_id=languages[selected_language])
            st.audio(audio_bytes, format="audio/wav")
        else:
            st.warning("Please enter a query.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
