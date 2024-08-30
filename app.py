import streamlit as st
from pages.accueil import page_accueil
from pages.register import page_register
from pages.welcome import page_welcome

# Initialize the page state
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# Display the page based on the state
if st.session_state.page == "accueil":
    page_accueil()
elif st.session_state.page == "register":
    page_register()
elif st.session_state.page == "welcome":
    page_welcome()
