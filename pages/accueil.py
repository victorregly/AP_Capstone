import streamlit as st
from utils.user_management import check_user
from utils.playlist_management import load_user_playlist, get_song_details

# Contenu principal de l'application

# Contenu principal de l'application
st.title("Welcome on Music streaming !")

def page_accueil():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        if check_user(username, password):
            st.session_state.page = "welcome"
            st.session_state.username = username
            
            # Load the user's playlist from the CSV
            user_playlist_song_ids = load_user_playlist(username)
            st.session_state.playlist = get_song_details(user_playlist_song_ids)
        else:
            st.error("Invalid username or password.")
    
    st.write("Don't have an account? [Create one](#)", unsafe_allow_html=True)
    if st.button("Create an Account"):
        st.session_state.page = "register"
