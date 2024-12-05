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

st.markdown("""
    <style>
    /* General Styling */
    body {
        background-color: #f9f9f9;
        font-family: 'Montserrat', sans-serif;
        color: #333;
    }
    
    /* Title Section */
    .title {
        text-align: center;
        color: #e50914;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 30px;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    }
    
    /* Subtitle for recommendation */
    .recommend-title {
        text-align: center;
        color: #00c853;
        font-size: 2.8rem;
        margin: 40px 0 20px;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }

    /* Movie name styling */
    .movie-name {
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        color: #555;
        margin: 10px 0;
    }

    /* Buttons Styling */
    .stButton button {
        background-color: #e50914 !important;
        color: #fff !important;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }

    .stButton button:hover {
        background-color: #b20710 !important;
        transform: translateY(-2px);
        box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.15);
    }

    /* Image Styling */
    .stImage img {
        border-radius: 10px;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .stImage img:hover {
        transform: scale(1.05);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.25);
    }

    /* Recommendation Section Styling */
    .stSelectbox {
        margin-bottom: 20px;
    }

    /* Columns Styling */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Error & Success Styling */
    .stAlert {
        border-radius: 10px;
        margin-top: 10px;
    }

    .stAlert div[role='alert'] {
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>Welcome to Ibrahim's Movie Recommender 🎬</h1>", unsafe_allow_html=True)



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

