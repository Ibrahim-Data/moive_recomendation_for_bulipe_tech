import streamlit as st
import pandas as pd
import pickle
import requests
from difflib import get_close_matches

# Set page config for the tab title and emoji
st.set_page_config(page_title="Movie Recommendation System 🎬", page_icon="🎬")

st.markdown("""
    <style>
        .movie-container {
            display: flex;
            justify-content: space-evenly; /* Even spacing between movies */
            align-items: flex-start; /* Align items to the top */
            flex-wrap: wrap; /* Allow wrapping if the screen is small */
            gap: 20px; /* Add spacing between items */
            margin-top: 20px;
        }
        .movie-box {
            text-align: center;
            width: 18%; /* Set fixed width for consistent appearance */
            border: 2px solid #ddd;
            padding: 10px;
            border-radius: 10px;
            background: #fff;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        }
        .movie-title {
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Page header
st.markdown('<h1 style="text-align: center; color: #ff4b4b;">Welcome to Ibrahim Creation 🎬</h1>', unsafe_allow_html=True)
st.image('moive.jpg', use_column_width=True)

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
        st.error(f"No movies found similar to '{movie}'. Please try again.")
        return [], []

    closest_match = close_matches[0]
    st.success(f"🎉 We've found a match: **{closest_match}** 🍿")
    movies_index = moives[moives['title'] == closest_match].index[0]
    distances = similarity[movies_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_posters = []
    recommended_movie_titles = []
    for i in movie_list:
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

# Movie input: type or select
st.markdown('<h2 style="text-align: center; color: #333;">Find Your Next Favorite Movie!</h2>', unsafe_allow_html=True)
movie_input = st.text_input("Search for a movie:", placeholder="Type a movie name or select from the dropdown")
if not movie_input:
    movie_input = st.selectbox("Or select a movie from the list:", moives['title'].values)

if st.button('Show Recommendations'):
    if movie_input:
        posters, titles = recommendation(movie_input)
        if titles:
            # Begin flexbox container
            st.markdown('<div class="movie-container">', unsafe_allow_html=True)
            for poster, title in zip(posters, titles):
                # Add individual movie boxes
                st.markdown(f"""
                    <div class="movie-box">
                        <img src="{poster}" style="border-radius: 10px; width: 100%; height: auto;" />
                        <p class="movie-title">{title}</p>
                    </div>
                """, unsafe_allow_html=True)
            # End flexbox container
            st.markdown('</div>', unsafe_allow_html=True)


