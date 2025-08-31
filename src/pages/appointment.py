import streamlit as st
from services.whisper_stt import speech_to_text, store_audio_in_mongo
from services.murfservice import stream_tts_to_bytes, translate_texts_to_buffer
from pymongo import MongoClient
import os
from urllib.parse import parse_qs

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vitavoice"]
meetings_col = db["meetings"]

def get_or_create_meeting(room_id, patient, doctor):
    meeting = meetings_col.find_one({"room_id": room_id})
    if not meeting:
        meetings_col.insert_one({
            "room_id": room_id,
            "patient": patient,
            "doctor": doctor,
            "messages": []
        })
        meeting = meetings_col.find_one({"room_id": room_id})
    return meeting

def add_message(room_id, sender, audio_bytes, text, translated):
    meetings_col.update_one(
        {"room_id": room_id},
        {"$push": {"messages": {
            "from": sender,
            "audio": audio_bytes,
            "text": text,
            "translated": translated
        }}}
    )

def app():
    # Read query params for room and doctor
    query_params = st.query_params
    room_id = query_params.get("room", [None])[0]
    doctor_username = query_params.get("doctor", [None])[0]

    # Use session state for meeting info if available, else from query params
    username = st.session_state.get("username", "")
    role = st.session_state.get("role", None)
    selected_doctor = st.session_state.get("selected_doctor", doctor_username)

    if room_id and "meeting_room_id" not in st.session_state:
        st.session_state.meeting_room_id = room_id
        st.session_state.selected_doctor = doctor_username

    # If not already in a meeting, let user join/create one
    if "meeting_room_id" not in st.session_state:
        st.subheader("Join or Create a Meeting Room")
        room_id = st.text_input("Enter Meeting Room ID", value=room_id or "")
        if role == "patient":
            doctor_username = selected_doctor or st.text_input("Doctor's username", value=doctor_username or "")
            patient_username = username
        else:
            doctor_username = username
            patient_username = st.text_input("Patient's username")
        if st.button("Join Meeting"):
            st.session_state.meeting_room_id = room_id
            st.session_state.meeting_role = role
            st.session_state.meeting_patient = patient_username
            st.session_state.meeting_doctor = doctor_username
            st.rerun()
        return

    # Meeting info from session
# Meeting info from session, with defaults if missing
    room_id = st.session_state.get("meeting_room_id")
    role = st.session_state.get("meeting_role", st.session_state.get("role"))
    patient_username = st.session_state.get("meeting_patient", st.session_state.get("username") if role == "patient" else "")
    doctor_username = st.session_state.get("meeting_doctor", st.session_state.get("selected_doctor", ""))

    other_user = doctor_username if role == "patient" else patient_username
    meeting = get_or_create_meeting(room_id, patient_username, doctor_username)

# Place this here:
    role_display = role.capitalize() if role else "Unknown"
    st.success(f"Joined meeting room: {room_id} as {role_display}")
    # Show conversation history
    st.markdown("### Conversation")
    for msg in meeting["messages"]:
        who = "You" if msg["from"] == role else other_user
        st.markdown(f"**{who} ({msg['from']}):** {msg['translated']}")
        st.audio(msg["audio"], format="audio/wav")

    # Language selection (for demo, you can automate this)
    st.markdown("#### Language Settings")
    if role == "patient":
        your_lang = st.selectbox("Your Language", ["English", "Hindi"], key="pat_lang")
        other_lang = st.selectbox("Doctor's Language", ["English", "Hindi"], key="doc_lang")
    else:
        your_lang = st.selectbox("Your Language", ["English", "Hindi"], key="doc_lang")
        other_lang = st.selectbox("Patient's Language", ["English", "Hindi"], key="pat_lang")

    # Record and send message
    st.markdown("#### Speak and send your message:")
    audio_file = st.file_uploader("Record or upload your message (WAV/MP3)", type=["wav", "mp3"])
    if audio_file:
        # Store audio in MongoDB
        audio_id = store_audio_in_mongo(username, audio_file)
        text = speech_to_text(audio_id)
        st.write("Recognized:", text)

        # Translate to other user's language
        lang_map = {"English": "en-UK-ruby", "Hindi": "hi-IN-ayushi"}
        target_lang = other_lang
        target_voice = lang_map.get(target_lang, "en-UK-ruby")

        translated = translate_texts_to_buffer([text], target_language=target_lang)
        translated_text = translated.translations[0].translated_text

        # TTS for other user
        audio_tts = stream_tts_to_bytes(translated_text, voice_id=target_voice)
        st.audio(audio_tts, format="audio/wav")
        st.success(f"{other_user} hears: {translated_text}")

        # Save message to meeting
        add_message(room_id, role, audio_tts.getvalue(), text, translated_text)
        st.rerun()

    # Option to leave meeting
    if st.button("Leave Meeting"):
        for key in ["meeting_room_id", "meeting_role", "meeting_patient", "meeting_doctor"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "Dashboard"
        st.rerun()