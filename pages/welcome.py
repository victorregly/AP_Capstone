import streamlit as st
import pandas as pd
import os
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from utils.playlist_management import load_user_playlist, get_song_details, add_song_to_playlist, remove_song_from_playlist

MUSIC_DATA_FILE = 'data/dataset1.csv'

def recommend_songs(user_playlist, music_df, num_recommendations=5):
    if not user_playlist:
        return []

    # Define the numerical features for recommendation
    numerical_features = ['danceability', 'energy', 'valence', 'tempo', 
                          'acousticness', 'popularity', 'loudness', 
                          'speechiness']

    # Scale the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(music_df[numerical_features])

    # Filter out songs already in the playlist
    playlist_song_ids = [song['song_id'] for song in user_playlist]
    available_songs_df = music_df[~music_df['song_id'].isin(playlist_song_ids)]

    if available_songs_df.empty:
        return []  # No songs left to recommend

    # Calculate the centroid of the songs in the playlist
    playlist_indices = music_df.index[music_df['song_id'].isin(playlist_song_ids)].tolist()
    playlist_features = scaled_features[playlist_indices]
    centroid = playlist_features.mean(axis=0).reshape(1, -1)

    # Find nearest neighbors to the centroid
    nbrs = NearestNeighbors(n_neighbors=num_recommendations + len(playlist_song_ids), algorithm='auto').fit(scaled_features)
    distances, indices = nbrs.kneighbors(centroid)

    # Filter out songs that are already in the playlist
    recommended_indices = [index for index in indices[0] if music_df.iloc[index]['song_id'] not in playlist_song_ids]

    # Get the top recommended tracks, ensuring we have exactly `num_recommendations` songs
    recommended_tracks = music_df.iloc[recommended_indices][['song_id', 'artist', 'song_name']].head(num_recommendations)
    
    return recommended_tracks.to_dict('records')

def page_welcome():
    st.title(f"Welcome, {st.session_state.username}!")
    
    if 'playlist' not in st.session_state or not st.session_state.playlist:
        user_playlist_song_ids = load_user_playlist(st.session_state.username)
        st.session_state.playlist = get_song_details(user_playlist_song_ids)

    if os.path.exists(MUSIC_DATA_FILE):
        music_df = pd.read_csv(MUSIC_DATA_FILE)
    else:
        st.error("The music file is missing.")
        return
    
    st.subheader("Add Songs to Your Playlist")
    search_query = st.text_input("Search for a song to add to your playlist")

    if search_query:
        filtered_songs = music_df[
            music_df['song_name'].str.contains(search_query, case=False, na=False) |
            music_df['artist'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_songs = music_df
    
    filtered_songs = filtered_songs.sort_values(by='popularity', ascending=False)
    
    song_options = filtered_songs['song_name'] + " - " + filtered_songs['artist']

    if not song_options.empty:
        selected_song = st.selectbox("Select a song to add to your playlist", options=song_options)

        if st.button("Add to Playlist"):
            song_id = filtered_songs.loc[song_options == selected_song, 'song_id'].values[0]
            if song_id not in [song['song_id'] for song in st.session_state.playlist]:
                song_info = filtered_songs.loc[filtered_songs['song_id'] == song_id, ['song_id', 'song_name', 'artist']].iloc[0]
                st.session_state.playlist.append(song_info.to_dict())
                add_song_to_playlist(st.session_state.username, song_id)
                # Trigger a rerun by modifying the query params
                st.query_params['rerun'] = True
            else:
                st.warning(f"'{selected_song}' is already in your playlist.")
    else:
        st.write("No songs match your search. Please try a different query.")
    
    st.subheader("Your Playlist")
    if st.session_state.playlist:
        for song in st.session_state.playlist:
            col1, col2 = st.columns([4, 1])
            col1.write(f"{song['song_name']} - {song['artist']}")
            if col2.button("Remove", key=f"remove_{song['song_id']}"):
                st.session_state.playlist = [s for s in st.session_state.playlist if s['song_id'] != song['song_id']]
                remove_song_from_playlist(st.session_state.username, song['song_id'])
                # Trigger a rerun by modifying the query params
                st.query_params['rerun'] = True
    else:
        st.write("Your playlist is empty.")
    
    st.subheader("Recommended Songs")
    if st.session_state.playlist:
        recommended_tracks = recommend_songs(st.session_state.playlist, music_df)
        if recommended_tracks:
            for rec_song in recommended_tracks:
                col1, col2 = st.columns([4, 1])
                col1.write(f"{rec_song['song_name']} - {rec_song['artist']}")
                if col2.button("Add to Playlist", key=f"add_{rec_song['song_id']}"):
                    if rec_song['song_id'] not in [song['song_id'] for song in st.session_state.playlist]:
                        st.session_state.playlist.append(rec_song)
                        add_song_to_playlist(st.session_state.username, rec_song['song_id'])
                        # Trigger a rerun by modifying the query params
                        st.query_params['rerun'] = True
        else:
            st.write("No recommended songs available.")
    else:
        st.write("Add some songs to your playlist to get recommendations!")

    # Plotting the mean of scaled numerical features for songs in the playlist
    if st.session_state.playlist:
        st.subheader("Average Playlist Characteristics")
        
        # Extract the numerical features for songs in the playlist
        playlist_song_ids = [song['song_id'] for song in st.session_state.playlist]
        playlist_df = music_df[music_df['song_id'].isin(playlist_song_ids)]
        
        # Calculate the mean of the numerical features
        numerical_features = ['danceability', 'energy', 'valence', 'tempo', 
                              'acousticness', 'popularity', 'loudness', 
                              'speechiness']
        mean_features = playlist_df[numerical_features].mean()
        
        # Scale the mean features between -100 and 100
        scaler = MinMaxScaler(feature_range=(-100, 100))
        scaled_mean_features = scaler.fit_transform(mean_features.values.reshape(-1, 1))
        scaled_mean_features = scaled_mean_features.flatten().round().astype(int)
        
        # Create a DataFrame for plotting
        mean_features_df = pd.DataFrame(scaled_mean_features, index=numerical_features, columns=['Mean Value'])
        
        # Plot the data
        st.area_chart(mean_features_df)

    if st.button("Logout"):
        st.session_state.page = "accueil"
        del st.session_state['username']
        del st.session_state['playlist']
