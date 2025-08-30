import streamlit as st
from services.engine import queries
from services.murfservice import stream_tts_to_bytes

def app():
    st.title("Dashboard")
    st.success(f"Welcome, {st.session_state.username}!")
    
    user_query = st.text_input("Enter your query:", key="user_query")
    if st.button("Submit Query"):
        if user_query.strip():
            result = queries(st.session_state.username, user_query)
            audio_bytes = stream_tts_to_bytes(str(result), voice_id="en-IN-arohi")
            st.audio(audio_bytes, format="audio/wav")
        else:
            st.warning("Please enter a query.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
