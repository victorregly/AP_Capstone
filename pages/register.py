import streamlit as st
from utils.user_management import add_user

def page_register():
    st.title("Create an Account")
    
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    
    if st.button("Sign Up"):
        result = add_user(new_username, new_password)
        
        if result == "success":
            st.success("Account created successfully! You can now log in.")
            st.session_state.page = "accueil"
        elif result == "exists":
            st.error("Username already exists. Please choose a different username.")
        elif result == "empty_username":
            st.error("Username cannot be empty or contain only spaces.")
        elif result == "empty_password":
            st.error("Password cannot be empty or contain only spaces.")
        elif result == "invalid_username":
            st.error("Username cannot contain spaces. Please enter a valid username.")
        elif result == "invalid_password":
            st.error("Password cannot contain spaces. Please enter a valid password.")
