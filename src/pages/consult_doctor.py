import streamlit as st

def app():
    st.title("Book a Doctor Consultation")

    # Example: List of available doctors (replace with DB query)
    doctors = [
        {"name": "Dr. A. Sharma", "specialty": "General Physician", "lang": "English"},
        {"name": "Dr. B. Rao", "specialty": "Cardiologist", "lang": "Telugu"},
    ]
    doctor_names = [f"{doc['name']} ({doc['specialty']}, {doc['lang']})" for doc in doctors]
    selected = st.selectbox("Choose a doctor", doctor_names)
    st.write("Selected:", selected)

    if st.button("Start Appointment"):
        st.session_state.selected_doctor = selected
        st.session_state.page = "Appointment"
        st.rerun()