import streamlit as st
import pandas as pd
import pickle
import requests
from difflib import get_close_matches

# Set page config for the tab title and emoji
st.set_page_config(page_title="Movie Recommendation System 🎬", page_icon="🎬")

st.title('Welcome To Ibrahim Creation ')
st.title('🎬 Welcome To Ibrahim Creation ')
st.image('moive.jpg')

# Function to fetch poster from the movie API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', None)
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

# Recommendation function with fuzzy matching
def recommendation(movie):
    try:
        # Check for close matches in case of spelling mistakes
        close_matches = get_close_matches(movie, moives['title'], n=5, cutoff=0.6)

        if not close_matches:
            st.error(f"Movie '{movie}' not found. Please try again.")
            return

        # If close matches are found, use the closest one
        closest_match = close_matches[0]
        st.success(f"🎉 Great choice! We've found a close match for you: **{closest_match}** 🍿")

        # Find index of the closest match
        movies_index = moives[moives['title'] == closest_match].index[0]
        distance = similarity[movies_index]
        movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

        # Collect movie titles and posters
        movie_titles = []
        recommended_movie_posters = []
        for i in movies_list:
            movie_id = moives.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            movie_titles.append(moives.iloc[i[0]].title)

        return recommended_movie_posters, movie_titles

    except IndexError:
        st.error("Movie not found or not enough data.")

# Movie Recommendation System Section Title
st.title("Movie Recommendation System")

# Load models and data
model_path = r"/mount/src/moive-recommender-system/models/movie_dict.pkl"
similarity_path = r"/mount/src/moive-recommender-system/models/similarity1.pkl"

with open(model_path, 'rb') as model_file:
    movies_dict = pickle.load(model_file)
moives = pd.DataFrame(movies_dict)

with open(similarity_path, 'rb') as similarity_file:
    similarity = pickle.load(similarity_file)


# User input: both selectbox and text input
selected_movie_name = st.selectbox(
    'Select a movie from the list:',
    moives['title'].values
)

manual_movie_name = st.text_input(
    "Or type a movie name manually:"
)

# Use manual input if provided, otherwise use the selected one
final_movie_name = manual_movie_name if manual_movie_name else selected_movie_name

# Show Recommendations Button
if st.button('Show Recommendations'):
    if final_movie_name:
        recommended_movie_posters, recommended_movie_titles = recommendation(final_movie_name)

        if recommended_movie_titles:
            # Display recommendations in columns
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.text(recommended_movie_titles[0])
                st.image(recommended_movie_posters[0])

            with col2:
                st.text(recommended_movie_titles[1])
                st.image(recommended_movie_posters[1])

            with col3:
                st.text(recommended_movie_titles[2])
                st.image(recommended_movie_posters[2])

            with col4:
                st.text(recommended_movie_titles[3])
                st.image(recommended_movie_posters[3])

            with col5:
                st.text(recommended_movie_titles[4])
                st.image(recommended_movie_posters[4])
    else:
        st.warning("Please select or type a movie.")
