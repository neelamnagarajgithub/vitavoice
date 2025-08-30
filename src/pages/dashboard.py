import streamlit as st
from services.engine import queries  # Make sure this function exists

def app():
    st.title("Dashboard")
    st.success(f"Welcome, {st.session_state.username}!")
    
    # Input for user query
    user_query = st.text_input("Enter your query:", key="user_query")
    if st.button("Submit Query"):
        if user_query.strip():
            result = queries(st.session_state.username, user_query)
            st.write("Result:")
            st.write(result)
        else:
            st.warning("Please enter a query.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
