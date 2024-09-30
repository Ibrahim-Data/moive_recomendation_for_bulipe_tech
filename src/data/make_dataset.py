import pandas as pd

def load_data(movie_path: str, credits_path: str):
    movie = pd.read_csv(movie_path)[:1000]
    credits = pd.read_csv(credits_path)[:1000]
    return movie, credits

def preprocess_data(movie, credits):
    movies1 = movie.merge(credits)
    movies = movies1[["movie_id", "keywords", "overview", "title", "cast", "genres", "crew"]]
    movies.dropna(inplace=True)
    return movies

def main():
    movie, credits = load_data(r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\data\raw\tmdb_5000_movies.csv",r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\data\raw\tmdb_5000_credits.csv")
    movies = preprocess_data(movie, credits)
    movies.to_csv("E:\Work files\movie-recommendation-system\Movie-Recommendation-System\data\processed\processed_movies.csv", index=False)

if __name__ == "__main__":
    main()
