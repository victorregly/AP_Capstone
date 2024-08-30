import streamlit as st
import pandas as pd
import os

# Define file paths
USER_DATA_FILE = 'data/users.csv'
MUSIC_DATA_FILE = 'data/music.csv'
PLAYLIST_DATA_FILE = 'data/playlists.csv'

# Function to check if a user exists
def check_user(username, password):
    if os.path.exists(USER_DATA_FILE):
        users_df = pd.read_csv(USER_DATA_FILE)
        user_row = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
        return not user_row.empty
    else:
        return False

# Function to add a new user
def add_user(username, password):
    if os.path.exists(USER_DATA_FILE):
        users_df = pd.read_csv(USER_DATA_FILE)
        new_user_df = pd.DataFrame([[username, password]], columns=['username', 'password'])
        users_df = pd.concat([users_df, new_user_df], ignore_index=True)
    else:
        users_df = pd.DataFrame([[username, password]], columns=['username', 'password'])
    users_df.to_csv(USER_DATA_FILE, index=False)

# Function to load a user's playlist
def load_user_playlist(username):
    if os.path.exists(PLAYLIST_DATA_FILE):
        playlists_df = pd.read_csv(PLAYLIST_DATA_FILE)
        user_playlist = playlists_df[playlists_df['username'] == username]['song_id'].tolist()
        return user_playlist
    else:
        return []

# Function to add a song to a user's playlist
def add_song_to_playlist(username, song_id):
    if os.path.exists(PLAYLIST_DATA_FILE):
        playlists_df = pd.read_csv(PLAYLIST_DATA_FILE)
    else:
        playlists_df = pd.DataFrame(columns=['username', 'song_id'])
    
    # Add the new song to the user's playlist if not already present
    if not ((playlists_df['username'] == username) & (playlists_df['song_id'] == song_id)).any():
        new_entry = pd.DataFrame([[username, song_id]], columns=['username', 'song_id'])
        playlists_df = pd.concat([playlists_df, new_entry], ignore_index=True)
        playlists_df.to_csv(PLAYLIST_DATA_FILE, index=False)

# Function to remove a song from a user's playlist
def remove_song_from_playlist(username, song_id):
    if os.path.exists(PLAYLIST_DATA_FILE):
        playlists_df = pd.read_csv(PLAYLIST_DATA_FILE)
        playlists_df = playlists_df[~((playlists_df['username'] == username) & (playlists_df['song_id'] == song_id))]
        playlists_df.to_csv(PLAYLIST_DATA_FILE, index=False)

# Function to get song details from song IDs
def get_song_details(song_ids):
    if os.path.exists(MUSIC_DATA_FILE):
        music_df = pd.read_csv(MUSIC_DATA_FILE)
        song_details = music_df[music_df['song_id'].isin(song_ids)].to_dict('records')
        return song_details
    else:
        st.error("The music file is missing.")
        return []

# Login page
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
            st.session_state.playlist = get_song_details(user_playlist_song_ids)  # Load song details
            
        else:
            st.error("Invalid username or password.")
    
    st.write("Don't have an account? [Create one](#)", unsafe_allow_html=True)
    if st.button("Create an Account"):
        st.session_state.page = "register"

# Registration page
def page_register():
    st.title("Create an Account")
    
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    
    if st.button("Sign Up"):
        add_user(new_username, new_password)
        st.success("Account created successfully! You can now log in.")
        st.session_state.page = "accueil"

# Welcome page with playlist management
def page_welcome():
    st.title(f"Welcome, {st.session_state.username}!")
    
    # Load user's playlist from the CSV (if not already loaded)
    if 'playlist' not in st.session_state or not st.session_state.playlist:
        user_playlist_song_ids = load_user_playlist(st.session_state.username)
        st.session_state.playlist = get_song_details(user_playlist_song_ids)  # Load song details

    # Load song data
    if os.path.exists(MUSIC_DATA_FILE):
        music_df = pd.read_csv(MUSIC_DATA_FILE)
    else:
        st.error("The music file is missing.")
        return
    
    # Search input for filtering songs
    st.subheader("Add Songs to Your Playlist")
    search_query = st.text_input("Search for a song to add to your playlist")

    # Filter songs based on the search query
    if search_query:
        filtered_songs = music_df[
            music_df['song_name'].str.contains(search_query, case=False, na=False) |
            music_df['artist'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_songs = music_df
    
    # Convert filtered songs to a list for the selectbox
    song_options = filtered_songs['song_name'] + " - " + filtered_songs['artist']

    # If there are filtered songs, show them in a dropdown
    if not song_options.empty:
        selected_song = st.selectbox(
            "Select a song to add to your playlist",
            options=song_options
        )

        # Add selected song to the playlist
        if st.button("Add to Playlist"):
            song_id = filtered_songs.loc[song_options == selected_song, 'song_id'].values[0]
            if song_id not in [song['song_id'] for song in st.session_state.playlist]:
                # Add song details to session state playlist
                st.session_state.playlist.append({
                    'song_id': song_id,
                    'song_name': filtered_songs.loc[filtered_songs['song_id'] == song_id, 'song_name'].values[0],
                    'artist': filtered_songs.loc[filtered_songs['song_id'] == song_id, 'artist'].values[0]
                })
                add_song_to_playlist(st.session_state.username, song_id)  # Add to CSV
                st.session_state.page = "welcome"  # Force reload without rerun
                return  # Exit the function to force reload
            else:
                st.warning(f"'{selected_song}' is already in your playlist.")
    else:
        st.write("No songs match your search. Please try a different query.")
    
    # Display the user's playlist with remove option
    st.subheader("Your Playlist")
    if st.session_state.playlist:
        for song in st.session_state.playlist:
            col1, col2 = st.columns([4, 1])
            col1.write(f"{song['song_name']} - {song['artist']}")
            if col2.button("Remove", key=f"remove_{song['song_id']}"):
                st.session_state.playlist = [s for s in st.session_state.playlist if s['song_id'] != song['song_id']]
                remove_song_from_playlist(st.session_state.username, song['song_id'])  # Remove from CSV
                st.session_state.page = "welcome"  # Force reload without rerun
                return  # Exit the function to force reload
    else:
        st.write("Your playlist is empty.")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.page = "accueil"
        del st.session_state['username']
        del st.session_state['playlist']
        return  # Exit to reload the login page



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
