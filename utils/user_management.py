import pandas as pd
import os

USER_DATA_FILE = 'data/users.csv'

def check_user(username, password):
    if os.path.exists(USER_DATA_FILE):
        users_df = pd.read_csv(USER_DATA_FILE)
        user_row = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
        return not user_row.empty
    else:
        return False

def add_user(username, password):
    # Check if the username is empty or contains only spaces
    if not username.strip():
        return "empty_username"  # Indicate that the username is empty or only spaces
    
    # Check if the password is empty or contains only spaces
    if not password.strip():
        return "empty_password"  # Indicate that the password is empty or only spaces

    # Check if the username contains any spaces
    if " " in username:
        return "invalid_username"  # Indicate that the username contains spaces

    # Check if the password contains any spaces
    if " " in password:
        return "invalid_password"  # Indicate that the password contains spaces
    
    if os.path.exists(USER_DATA_FILE):
        users_df = pd.read_csv(USER_DATA_FILE)
        
        # Check if username already exists
        if username in users_df['username'].values:
            return "exists"  # Indicate that the username already exists
        
        new_user_df = pd.DataFrame([[username, password]], columns=['username', 'password'])
        users_df = pd.concat([users_df, new_user_df], ignore_index=True)
    else:
        users_df = pd.DataFrame([[username, password]], columns=['username', 'password'])
    
    users_df.to_csv(USER_DATA_FILE, index=False)
    return "success"  # Indicate successful creation
