import streamlit as st
from services.whisper_stt import speech_to_text, store_audio_in_mongo
from services.murfservice import stream_tts_to_bytes, translate_texts_to_buffer
def app():
    st.title("Live Doctor Consultation")
    st.info(f"Consulting with: {st.session_state.get('selected_doctor', 'Doctor')}")

    # Language selection for both users (simulate for demo)
    patient_lang = st.selectbox("Your Language", ["English", "Telugu"], key="pat_lang")
    doctor_lang = st.selectbox("Doctor's Language", ["English", "Telugu"], key="doc_lang")

    # Patient speaks
    st.markdown("#### You (Patient) speak:")
    patient_audio = st.audio_input("Record your question (Patient)")
    if patient_audio:
        # STT
        audio_id = store_audio_in_mongo(st.session_state.username, patient_audio)
        text = speech_to_text(audio_id)
        st.write("Recognized:", text)
        # Translate to doctor's language
        if patient_lang != doctor_lang:
            translated = translate_texts_to_buffer([text], target_language=doctor_lang)
            translated_text = translated.translations[0].translated_text
        else:
            translated_text = text
        # TTS for doctor
        audio_bytes = stream_tts_to_bytes(translated_text, voice_id="en-UK-ruby" if doctor_lang == "English" else "hi-IN-ayushi")
        st.audio(audio_bytes, format="audio/wav")
        st.success(f"Doctor hears: {translated_text}")

    # Doctor speaks (simulate for demo)
    st.markdown("#### Doctor speaks:")
    doctor_audio = st.audio_input("Record doctor's reply")
    if doctor_audio:
        audio_id = store_audio_in_mongo(st.session_state.username, doctor_audio)
        text = speech_to_text(audio_id)
        st.write("Recognized:", text)
        # Translate to patient's language
        if doctor_lang != patient_lang:
            translated = translate_texts_to_buffer([text], target_language=patient_lang)
            translated_text = translated.translations[0].translated_text
        else:
            translated_text = text
        audio_bytes = stream_tts_to_bytes(translated_text, voice_id="en-UK-ruby" if patient_lang == "English" else "hi-IN-ayushi")
        st.audio(audio_bytes, format="audio/wav")
        st.success(f"Patient hears: {translated_text}")