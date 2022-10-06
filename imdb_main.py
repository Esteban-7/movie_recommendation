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
    #Finds the link and ID to the imdb page of a movie by searching for it using the search movies module (selenium module)
    #Given the ID of the chosen movie, a new movie object is created using the movie_info module, gathering the features of the film with beautiful soup
    #Calls the get_imdb_recommendations module, which scraps the webpage of a film to gather the "more like this" recommendations by imdb's system
    #Calls on the scrap_imdb and passes the genres of the movie as the argument. Creating a long list of movies with the same set of genres.
    movie_id = search_movies(path)[1]
    movie = get_movie_info(movie_id)
    
    imdb_recommendations = get_imdb_recommendations(movie_id,2)
    movie["imdb_recommendations"]=imdb_recommendations
    print(movie)

    scrap_new_recommended = scrap_imdb(genres = movie["genres"])
    if scrap_new_recommended == True:
       with open("imdb_scraper/imdb_scraper/spiders/recommended.json","r") as f:
            data = json.load(f) 
    new_recommendations = data
    movie["new_recommendations"]  = new_recommendations
    return movie

def recommend():
    #make the script run, creates a movie element and uploads its information, as well as the recommendations information to the mongoDB database
    #generates a temp file called imdb_movie_id in which the id of the film is saved for it to be read later by the streamlit module.
    try:
        movie_test = new_movie()
        save_movie(movie_test)
        upload_recommended_infos(movie_test)
    

        with open("imdb_id_movie.json","w") as f:
            json.dump({"imdb_movie_id": movie_test["imdb_id"]},f)
        return True
    except:
        print("Problemn in main function.")
        return False

recommend()

