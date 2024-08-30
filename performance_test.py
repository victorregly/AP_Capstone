import pandas as pd
import time
import tracemalloc
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from utils.playlist_management import get_song_details
from pages.welcome import recommend_songs

# Load the full music dataset
MUSIC_DATA_FILE = 'data/dataset1.csv'
music_df = pd.read_csv(MUSIC_DATA_FILE)

# Function to simulate different user playlists
def simulate_user_playlist(size, music_df):
    return music_df.sample(n=size)['song_id'].tolist()

# Function to measure performance
def measure_performance(playlist_sizes, music_df, num_recommendations=5):
    performance_results = []

    for size in playlist_sizes:
        print(f"Testing with playlist size: {size}")

        # Simulate a user playlist
        user_playlist_ids = simulate_user_playlist(size, music_df)
        user_playlist = get_song_details(user_playlist_ids)
        
        # Start measuring time
        start_time = time.time()

        # Start measuring memory usage
        tracemalloc.start()

        # Generate recommendations
        recommendations = recommend_songs(user_playlist, music_df, num_recommendations)

        # Stop measuring memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Stop measuring time
        end_time = time.time()

        # Calculate metrics
        response_time = end_time - start_time
        memory_usage = peak / 10**6  # Convert to MB

        # Store the results
        performance_results.append({
            'Playlist Size': size,
            'Response Time (s)': response_time,
            'Memory Usage (MB)': memory_usage,
            'Number of Recommendations': len(recommendations)
        })

    return pd.DataFrame(performance_results)

# Define playlist sizes to test
playlist_sizes = [10, 50, 100, 500, 1000]

# Run the performance tests
performance_results = measure_performance(playlist_sizes, music_df)

# Display the results
print(performance_results)

# Optionally, save the results to a CSV file for further analysis
performance_results.to_csv('performance_results.csv', index=False)
