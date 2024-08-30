import pandas as pd
import os

PLAYLIST_DATA_FILE = 'data/playlists.csv'
MUSIC_DATA_FILE = 'data/dataset1.csv'

def load_user_playlist(username):
    if os.path.exists(PLAYLIST_DATA_FILE):
        playlists_df = pd.read_csv(PLAYLIST_DATA_FILE)
        user_playlist = playlists_df[playlists_df['username'] == username]['song_id'].tolist()
        return user_playlist
    else:
        return []

def add_song_to_playlist(username, song_id):
    if os.path.exists(PLAYLIST_DATA_FILE):
        playlists_df = pd.read_csv(PLAYLIST_DATA_FILE)
    else:
        playlists_df = pd.DataFrame(columns=['username', 'song_id'])
    
    if not ((playlists_df['username'] == username) & (playlists_df['song_id'] == song_id)).any():
        new_entry = pd.DataFrame([[username, song_id]], columns=['username', 'song_id'])
        playlists_df = pd.concat([playlists_df, new_entry], ignore_index=True)
        playlists_df.to_csv(PLAYLIST_DATA_FILE, index=False)

def remove_song_from_playlist(username, song_id):
    if os.path.exists(PLAYLIST_DATA_FILE):
        playlists_df = pd.read_csv(PLAYLIST_DATA_FILE)
        playlists_df = playlists_df[~((playlists_df['username'] == username) & (playlists_df['song_id'] == song_id))]
        playlists_df.to_csv(PLAYLIST_DATA_FILE, index=False)

def get_song_details(song_ids):
    if os.path.exists(MUSIC_DATA_FILE):
        music_df = pd.read_csv(MUSIC_DATA_FILE)
        song_details = music_df[music_df['song_id'].isin(song_ids)].to_dict('records')
        return song_details
    else:
        return []
