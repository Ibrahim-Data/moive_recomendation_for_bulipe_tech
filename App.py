import streamlit as st
import pandas as pd
import pickle
import requests
from difflib import get_close_matches

# Set page configuration
st.set_page_config(
    page_title="Movie Recommendation System 🎬",
    page_icon="🎬",
    layout="wide",
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        color: #ff4c4c;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .recommend-title {
        text-align: center;
        color: #4caf50;
        font-size: 2.5rem;
        margin: 30px 0;
    }
    .movie-name {
        text-align: center;
        font-weight: bold;
        color: #000;
        margin: 10px 0;
    }
    .stButton button {
        background-color: #ff4c4c !important;
        color: white !important;
        border-radius: 5px;
    }
    .stImage {
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>Welcome to Ibrahim's Movie Recommender 🎬</h1>", unsafe_allow_html=True)

# Display header image
# Display header image with adjusted size
st.image("moive.jpg", use_column_width=False, width=200)  # Adjust 'width' as needed

# Function to fetch poster from the movie API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', None)
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

# Recommendation function with fuzzy matching
def recommendation(movie):
    close_matches = get_close_matches(movie, moives['title'], n=5, cutoff=0.6)
    if not close_matches:
        st.error(f"Movie '{movie}' not found. Please try again.")
        return [], []

    closest_match = close_matches[0]
    st.success(f"🎉 Great choice! We've found a close match for you: **{closest_match}** 🍿")
    
    movies_index = moives[moives['title'] == closest_match].index[0]
    distance = similarity[movies_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_titles = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = moives.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_titles.append(moives.iloc[i[0]].title)

    return recommended_movie_posters, recommended_movie_titles

# Load models and data
model_path = r"/mount/src/moive-recommender-system/models/movie_dict1.pkl"
similarity_path = r"/mount/src/moive-recommender-system/models/similarity.pkl"

with open(model_path, 'rb') as model_file:
    movies_dict = pickle.load(model_file)
moives = pd.DataFrame(movies_dict)

with open(similarity_path, 'rb') as similarity_file:
    similarity = pickle.load(similarity_file)

# Movie Recommendation System Section
st.markdown("<h2 class='recommend-title'>Find Your Next Favorite Movie 🍿</h2>", unsafe_allow_html=True)

# User input: unified input box with dropdown and text search
movie_input = st.selectbox(
    'Search or Select a Movie:',
    options=["Type or select a movie"] + list(moives['title'].values)
)

# Check if a movie is selected or typed
if movie_input != "Type or select a movie" and st.button('Show Recommendations'):
    recommended_movie_posters, recommended_movie_titles = recommendation(movie_input)

    if recommended_movie_titles:
        cols = st.columns(5)  # Display 5 movies in columns
        for idx, col in enumerate(cols):
            with col:
                if idx < len(recommended_movie_titles):
                    st.markdown(f"<div class='movie-name'>{recommended_movie_titles[idx]}</div>", unsafe_allow_html=True)
                    st.image(recommended_movie_posters[idx], use_column_width=True)

