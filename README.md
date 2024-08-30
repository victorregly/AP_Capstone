# Personalized Playlist Generation System
Capstone Project for Advanced Programming class.

## Overview

This project is a personalized playlist generation system that dynamically adapts to user preferences through a feedback-driven recommendation engine. The system leverages content-based filtering to generate recommendations based on a user's listening history and interactions, ensuring that the recommendations evolve in line with the user's changing tastes.

## Features

- **User Authentication**: Secure login and registration system with password hashing.
- **Dynamic User Profiles**: User profiles that evolve based on interactions, capturing preferences and listening history.
- **Recommendation System**: A content-based recommendation engine that suggests tracks using similarity scoring.
- **Feedback Loop**: Continuous refinement of recommendations based on user interactions.
- **Streamlit Interface**: A user-friendly desktop application interface built with Streamlit for managing playlists and exploring recommendations.

## Project Structure

- `app.py`: The main entry point of the Streamlit application, handling page navigation.
- `pages/`: Directory containing the Streamlit page components:
  - `accueil.py`: Login functionality.
  - `register.py`: User registration functionality.
  - `welcome.py`: Main application page for playlist management and song recommendations.
- `utils/`: Utility modules for user and playlist management:
  - `user_management.py`: Handles user authentication and registration.
  - `playlist_management.py`: Manages playlist operations and song retrieval.
- `data/`: Directory containing the dataset and user-related CSV files.
- `performance_test.py`: Script for conducting performance tests on the recommendation system, measuring response time and memory usage across different playlist sizes.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/playlist-generation-system.git
    cd playlist-generation-system
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Usage

- **Login/Register**: Start by creating an account or logging in with existing credentials.
- **Manage Playlists**: Add or remove songs from your playlist using the intuitive Streamlit interface.
- **Get Recommendations**: The system will suggest songs based on your current playlist. The more you interact, the better the recommendations.
- **View Playlist Characteristics**: Visualize the average characteristics of your playlist and understand your musical preferences.

## Performance Testing

Performance tests were conducted to evaluate the system's efficiency in terms of response time and memory usage. Below are some key results:

- **Response Time**: The system remains responsive even with larger playlists, with response times ranging from 0.124 to 0.524 seconds depending on playlist size.
- **Memory Usage**: Memory usage remained stable across tests, indicating good scalability.

To run your own performance tests, use the `performance_test.py` script included in the project.

## Helper Tools

This project leveraged several external tools to enhance productivity and maintain code quality:

- **ChatGPT**: Assisted in generating code snippets, drafting documentation, and solving complex programming challenges.
- **GitHub Copilot**: Provided real-time code suggestions and autocompletions, speeding up the development process and ensuring consistency across the codebase.

## Bibliography

- Schedl, M., Zamani, H., Chen, C. W., et al. (2018). Current challenges and visions in music recommender systems research. _International Journal of Multimedia Information Retrieval_, 7(2), 95–116. [https://doi.org/10.1007/s13735-018-0154-2](https://doi.org/10.1007/s13735-018-0154-2)

## Future Work

- **Advanced Algorithms**: Incorporating more sophisticated recommendation algorithms, such as deep learning-based models, to improve recommendation accuracy.
- **Database Integration**: Migrating from CSV files to a relational database for better scalability and data management.
- **Expanded Media Types**: Extending the recommendation system to include other types of media, such as podcasts or videos.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

---

Thank you for using the Personalized Playlist Generation System! If you have any questions or need further assistance, feel free to contact me.
