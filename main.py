from search_movie.search_movie import search_movies
from movie_info import get_movie_info
from imdb_recommendations import get_recommendations
from os import getcwd
import pymongo



path = getcwd() + "\driver\chromedriver"


movie_id = search_movies(path)[1]

movie = get_movie_info(movie_id)

imdb_recommendations = get_recommendations(movie_id,2)

movie["imdb_recommendations"]=imdb_recommendations

def save_movie(movie):
    client = pymongo.MongoClient("localhost",27017)
    db = client["movie_recommendations"]
    collection = db["movie"]
    collection.insert_one(movie)


save_movie(movie)
