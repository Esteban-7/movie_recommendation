from search_movie.search_movie import search_movies
from movie_info import get_movie_info
from imdb_recommendations import get_imdb_recommendations
from os import getcwd
from imdb_mongo import save_movie, upload_recommended_infos
from imdb_scraper.imdb_scraper.spiders.imdbSpider import scrap_imdb
import json


path = getcwd() + "\driver\chromedriver"

def new_movie():
    movie_id = search_movies(path)[1]
    movie = get_movie_info(movie_id)
    
    imdb_recommendations = get_imdb_recommendations(movie_id,2)
    movie["imdb_recommendations"]=imdb_recommendations
    print(movie)
    print(movie["genres"])
    print(movie["imdb_recommendations"])

    #scrap_imdb(genres = movie["genres"])
    scrap_new_recommended = scrap_imdb(genres = movie["genres"])
    if scrap_new_recommended == True:
       with open("imdb_scraper/imdb_scraper/spiders/recommended.json","r") as f:
            data = json.load(f) 
    new_recommendations = data
    movie["new_recommendations"]  = new_recommendations
    return movie

movie_test = new_movie()
save_movie(movie_test)
upload_recommended_infos(movie_test)
