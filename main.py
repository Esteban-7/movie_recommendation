from search_movie.search_movie import search_movies
from movie_info import get_movie_info
from imdb_recommendations import get_imdb_recommendations
from os import getcwd
from imdb_mongo import save_movie, upload_recommended_infos



path = getcwd() + "\driver\chromedriver"

def new_movie():
    movie_id = search_movies(path)[1]
    movie = get_movie_info(movie_id)
    imdb_recommendations = get_imdb_recommendations(movie_id,1)
    movie["imdb_recommendations"]=imdb_recommendations
    #new_recommendations = #
    #movie["new_recommendations"]  = new_recommendations
    return movie

movie = new_movie()
save_movie(movie)
upload_recommended_infos(movie)
