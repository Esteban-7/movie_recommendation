from search_movie.search_movie import search_movies
from movie_info import get_movie_info
from imdb_recommendations import get_imdb_recommendations
from os import getcwd
from imdb_mongo import save_movie, upload_recommended_infos, get_recommendations_mongo
from imdb_scraper.imdb_scraper.spiders.imdbSpider import scrap_imdb
import json
import pandas as pd
import streamlit as st
import streamlit as st
import plotly.figure_factory as ff
import plotly
import plotly.express as px
import plotly.io as pio


path = getcwd() + "\driver\chromedriver"

def new_movie():
    movie_id = search_movies(path)[1]
    movie = get_movie_info(movie_id)
    
    imdb_recommendations = get_imdb_recommendations(movie_id,2)
    movie["imdb_recommendations"]=imdb_recommendations
    print(movie)
    print(movie["genres"])
    print(movie["imdb_recommendations"])

    scrap_new_recommended = scrap_imdb(genres = movie["genres"])
    if scrap_new_recommended == True:
       with open("imdb_scraper/imdb_scraper/spiders/recommended.json","r") as f:
            data = json.load(f) 
    new_recommendations = data
    movie["new_recommendations"]  = new_recommendations
    return movie

def recommend():
    try:
        movie_test = new_movie()
        save_movie(movie_test)
        upload_recommended_infos(movie_test)
        #recommended = get_recommendations_mongo(movie_test)

        with open("imdb_id_movie.json","w") as f:
            json.dump({"imdb_movie_id": movie_test["imdb_id"]},f)
        return True
    except:
        print("Problemn in main function.")
        return False

recommend()

