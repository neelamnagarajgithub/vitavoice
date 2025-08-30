import streamlit as st
from services.auth import signup, login

def app():
    st.set_page_config(
        page_title="VitaVoice",
        layout="centered"
    )

    # --- HERO SECTION ---
    st.markdown("""
    <h1 style='text-align: center; margin-bottom: 0.2em;'>VitaVoice</h1>
    <h4 style='text-align: center; color: #555; margin-top: 0;'>Your Voice, Your Health</h4>
    <p style='text-align: center; color: #888; max-width: 600px; margin: auto;'>
        AI-powered healthcare voice assistant that listens, understands, and helps you stay healthy.
    </p>
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
            else:
                st.error(msg)

    st.divider()

    # --- FEATURES ---
    st.header("Features")
    st.markdown("""
    - Voice-powered consultations  
    - Personalized health dashboard  
    - Secure medical record storage  
    - AI-driven health insights  
    - Smart reminders for medicines  
    """)

    st.divider()

    # --- ABOUT ---
    st.header("About VitaVoice")
    st.write(
       "VitaVoice is a voice-powered healthcare assistant that enables users to track, manage, and understand their health through natural voice interactions. It integrates medical record storage, AI-driven health insights, and real-time voice analysis, making healthcare more accessible and personalized."
    )

    st.divider()

    # --- DASHBOARD PREVIEW ---
    st.header("Dashboard Preview")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://placehold.co/400x250?text=Health+Summary", caption="Health Summary")
    with col2:
        st.image("https://placehold.co/400x250?text=Trends+and+Insights", caption="Trends & Insights")
    st.info("Login to explore your personalized health assistant.")

    st.divider()

    # --- CONTACT ---
    st.header("Contact Us")
    st.write("Email: support@vitavoice.ai") 
    st.write("Website: www.vitavoice.ai")
    st.write("Phone: +91-98765-43210")
    st.success("Let's revolutionize healthcare together!")