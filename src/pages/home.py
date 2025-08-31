import streamlit as st
from services.auth import signup, login
from pages.dashboard import load_chat_history  

def app():
    st.set_page_config(
        page_title="VitaVoice",
        layout="centered"
    )

    # --- LOGO & HERO SECTION ---
    st.image("assets/logo.png", width=120)  # Logo at the top (adjust path if needed)
    st.markdown("""
    <h1 style='text-align: center; margin-bottom: 0.2em;'>VitaVoice</h1>
    <h4 style='text-align: center; color: #555; margin-top: 0;'>Your Voice, Your Health</h4>
    """, unsafe_allow_html=True)

    st.divider()

    # --- AUTHENTICATION TABS ---
    tab = st.tabs(["Login", "Sign Up"])
    with tab[0]:
        st.subheader("Login to your account")
        login_user = st.text_input("Username", key="login_user")
        login_pw = st.text_input("Password", type="password", key="login_pw")
        login_role = st.selectbox("Role", ["doctor", "patient"], key="login_role")
        if st.button("Login", key="login_btn"):
            success, msg = login(login_user, login_pw, login_role)
            if success:
                st.success(msg)
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.session_state.chat_history = load_chat_history(login_user)
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error(msg)
    with tab[1]:
        st.subheader("Create a new account")
        signup_user = st.text_input("Username", key="signup_user")
        signup_pw = st.text_input("Password", type="password", key="signup_pw")
        signup_role = st.selectbox("Role", ["doctor", "patient"], key="signup_role")
        if st.button("Sign Up", key="signup_btn"):
            success, msg = signup(signup_user, signup_pw, signup_role)
            if success:
                st.success(msg)
                st.session_state.logged_in = True
                st.session_state.username = signup_user
                st.session_state.role = signup_role
                if signup_role == "patient":
                    st.session_state.chat_history = load_chat_history(signup_user)
                else:
                    st.session_state.chat_history = []
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error(msg)

    st.divider()

    # --- WHAT'S NEW / ANNOUNCEMENTS ---
    st.header("What's New")
    st.markdown("""
    - **Automatic EHR Generation:** Instantly create downloadable Electronic Health Records from your chat history.
    - **AI Voice Conversations:** Talk to the AI doctor using your voice—powered by advanced Speech-to-Text (STT) and Text-to-Speech (TTS).
    - **Multilingual Support:** Converse in your preferred language and get real-time voice responses.
    - **Secure Data Handling:** All your health data is encrypted and private.
    """)

    st.divider()

    # --- HOW IT WORKS ---
    st.header("How It Works")
    st.markdown("""
    1. **Sign up or log in** as a patient or doctor.
    2. **Chat with the AI doctor** using voice or text—your speech is transcribed and understood by the AI.
    3. **Receive instant, natural-sounding voice replies** in your chosen language.
    4. **Download your EHR summary** generated from your conversation at any time.
    5. **Track your health insights** and revisit your chat history securely.
    """)

    st.divider()

    # --- WHY CHOOSE US ---
    st.header("Why Choose VitaVoice?")
    st.markdown("""
    - **Automatic EHR summaries** for every conversation.
    - **AI-powered, natural voice chat** with advanced TTS and STT.
    - **Multi-language support** for inclusive healthcare.
    - **Downloadable health records** for easy sharing and continuity of care.
    - **End-to-end encryption** for your privacy and security.
    """)

    st.divider()

    # --- CONTACT ---
    st.header("Contact Us")
    st.write("Email: support@vitavoice.ai") 
    st.write("Website: www.vitavoice.ai")
    st.write("Phone: +91-98765-43210")
    st.success("Let's revolutionize healthcare together!")