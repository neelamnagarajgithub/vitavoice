import streamlit as st
from pymongo import MongoClient
import os
from services.engine import recommend_doctors  # Import the LLM-based recommender
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vitavoice"]
doctors_col = db["doctors"]

def app():
    st.title("Book a Doctor Consultation")

    # Retrieve doctors from MongoDB
    doctors = list(doctors_col.find({}))
    if not doctors:
        st.warning("No doctors found in the database.")
        return

    # Recommend a doctor using LLM based on chat history
    recommended_doctors = []
    if st.button("Recommend a Doctor"):
        chat_history = st.session_state.get("chat_history", [])
        recommended_usernames = recommend_doctors(chat_history, doctors)
        print("LLM recommended usernames:", recommended_usernames)
        print("All doctor usernames in DB:", [doc["username"] for doc in doctors])
        recommended_doctors = [
            doc for doc in doctors
            if doc["username"].lower().strip() in [u.lower().strip() for u in recommended_usernames]
        ]
        print("Matched recommended doctors:", [doc["username"] for doc in recommended_doctors])
        predicted_specs = set(doc["specialization"] for doc in recommended_doctors)
        print("Predicted specializations:", predicted_specs)
        if recommended_doctors:
            st.success("Recommended Doctors:")
            doctor_names = [f"{doc['name']} ({doc['specialization']})" for doc in recommended_doctors]
            selected_idx = st.selectbox("Choose a doctor", range(len(doctor_names)), format_func=lambda i: doctor_names[i], key="rec_doc_select")
            selected_doc = recommended_doctors[selected_idx]
        else:
            st.info("No specific recommendation based on your chat history. Please select manually.")
            doctor_names = [f"{doc['name']} ({doc['specialization']})" for doc in doctors]
            selected_idx = st.selectbox("Choose a doctor", range(len(doctor_names)), format_func=lambda i: doctor_names[i], key="all_doc_select")
            selected_doc = doctors[selected_idx]
    else:
        doctor_names = [f"{doc['name']} ({doc['specialization']})" for doc in doctors]
        selected_idx = st.selectbox("Choose a doctor", range(len(doctor_names)), format_func=lambda i: doctor_names[i], key="all_doc_select")
        selected_doc = doctors[selected_idx]

    # Show additional details
    st.markdown("### Doctor Details")
    st.write(f"**Name:** {selected_doc['name']}")
    st.write(f"**Specialization:** {selected_doc['specialization']}")
    st.write(f"**Experience:** {selected_doc.get('experience', 'N/A')} years")
    st.write(f"**Hospital:** {selected_doc.get('hospital', 'N/A')}")
    st.write(f"**Email:** {selected_doc.get('email', 'N/A')}")
    st.write(f"**Phone:** {selected_doc.get('phone', 'N/A')}")

    if st.button("Book Appointment"):
        st.session_state.selected_doctor = selected_doc["username"]
        # Generate a unique meeting room ID
        meeting_room_id = str(uuid.uuid4())
        st.session_state.meeting_room_id = meeting_room_id
        st.session_state.page = "Appointment"
        # Show/shareable link
        base_url = os.getenv("BASE_URL", "http://localhost:8501")  # Set your deployed URL in .streamlit/secrets.toml
        share_link = f"{base_url}?room={meeting_room_id}&doctor={selected_doc['username']}"
        st.success("Share this link with your doctor to join the appointment:")
        st.code(share_link)
        st.rerun()