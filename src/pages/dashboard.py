import streamlit as st

def app():
    st.title("Dashboard")
    st.success(f"Welcome, {st.session_state.username}!")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
