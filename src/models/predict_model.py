import pandas as pd
import pickle

def recommend(movie: str, df: pd.DataFrame, similarity):
    """Recommend movies based on the cosine similarity of tags."""
    movie_index = df[df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    recommendations = [df.iloc[i[0]].title for i in distances]
    return recommendations

def main():
    # Load the necessary data and models
    with open(r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\models\movie_dict.pkl", "rb") as file:
        movie_dict = pickle.load(file)
    similarity = pickle.load(open(r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\models\similarity.pkl", "rb"))

    # Convert movie_dict back to a DataFrame
    movies = pd.DataFrame.from_dict(movie_dict)

    # Get recommendations for a sample movie
    movie_to_recommend = "Avatar"  # Replace with any movie title
    recommendations = recommend(movie_to_recommend, movies, similarity)
    
    print(f"Recommendations for {movie_to_recommend}:")
    for movie in recommendations:
        print(movie)

if __name__ == "__main__":
    main()
