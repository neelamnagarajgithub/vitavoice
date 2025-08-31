import streamlit as st
from pages import home, dashboard, consult_doctor, appointment

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

pages = ["Home", "Dashboard", "ConsultDoctor", "Appointment"]
current_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0

# Synchronize selectbox and session state
selected_page = st.sidebar.selectbox(
    "Go to",
    pages,
    index=current_index,
    key="sidebar_page"
)

# Only update session state if user changes selectbox
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# Use st.session_state.page everywhere
if st.session_state.page == "Home":
    home.app()
elif st.session_state.page == "Dashboard":
    if st.session_state.logged_in:
        dashboard.app()
    else:
        st.warning("Please log in to access the dashboard.")
elif st.session_state.page == "ConsultDoctor":
    consult_doctor.app()
elif st.session_state.page == "Appointment":
    appointment.app()