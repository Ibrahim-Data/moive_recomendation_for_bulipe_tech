import ast
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer

def transfer(obj):
    I = [i["name"] for i in ast.literal_eval(obj)]
    return I

def transfer3(obj):
    I = [i["character"] for i in ast.literal_eval(obj)[:3]]
    return I

def transfer5(obj):
    I = [i["name"] for i in ast.literal_eval(obj) if i['job'] == 'Director']
    return I

def transfer6(obj):
    return [i.replace(" ", "") for i in obj]

def feature_engineering(movies):
    movies['genres'] = movies['genres'].apply(transfer)
    movies['keywords'] = movies['keywords'].apply(transfer)
    movies['cast'] = movies['cast'].apply(transfer3)
    movies['crew'] = movies['crew'].apply(transfer5)

    movies["keywords"] = movies["keywords"].apply(transfer6)
    movies["cast"] = movies["cast"].apply(transfer6)
    movies["genres"] = movies["genres"].apply(transfer6)
    movies["crew"] = movies["crew"].apply(transfer6)
    
    movies["overview"] = movies["overview"].apply(lambda x: x.split())
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    new = movies.drop(columns=['overview', 'genres', 'keywords', 'cast', 'crew'])
    new['tags'] = new['tags'].apply(lambda x: " ".join(x))
    
    return new

def main():
    movies = pd.read_csv(r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\data\processed\processed_movies.csv")
    new = feature_engineering(movies)
    new.to_csv(r"E:\Work files\movie-recommendation-system\Movie-Recommendation-System\data\processed\features_movies.csv", index=False)

if __name__ == "__main__":
    main()
