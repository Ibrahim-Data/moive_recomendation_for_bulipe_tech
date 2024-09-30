import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def vectorize_text(df: pd.DataFrame, max_features: int = 5000) -> pd.DataFrame:
    """Convert text data into vectors using CountVectorizer."""
    cv = CountVectorizer(max_features=max_features, stop_words="english")
    vectors = cv.fit_transform(df['tags']).toarray()
    return vectors, cv

def calculate_similarity(vectors):
    """Calculate cosine similarity between vectors."""
    return cosine_similarity(vectors)

def save_model(obj, filepath: str):
    """Save a model or object using pickle."""
    with open(filepath, "wb") as file:
        pickle.dump(obj, file)

def main():
    # Load processed data
    movies = pd.read_csv(r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\data\processed\features_movies.csv")

    # Vectorize the tags column
    vectors, cv = vectorize_text(movies)

    # Calculate similarity
    similarity = calculate_similarity(vectors)

    # Save models and data
    save_model(movies.to_dict(), r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\models\movie_dict.pkl")
    save_model(similarity, r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\models\similarity.pkl")

if __name__ == "__main__":
    main()
