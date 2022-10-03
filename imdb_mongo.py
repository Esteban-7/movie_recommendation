import pymongo
from movie_info import info_recommendations


def save_movie(movie):
    client = pymongo.MongoClient("localhost",27017)
    db = client["movie_recommendations"]
    collection = db["movie"]
    collection.insert_one(movie)

def upload_recommended_infos(movie):
    client = pymongo.MongoClient("localhost",27017)
    db = client["movie_recommendations"]
    collection = db["movie_recommendation"]
    film = {"movie_id":movie["imdb_id"], 
            "imdb_recommended": info_recommendations(movie,"imdb")
            } 
    


    collection.insert_one(film)


def get_imdb_rec_mongo(movie):
    #gets a movie (dictionary of info), returns the list of dictionaries for all the movies recommended by imdb that were saved in the mongodatabase
    client = pymongo.MongoClient("localhost",27017)
    db = client["movie_recommendations"]
    collection = db["imdb_rec_temp"]
    doc = collection.find({"movie_id": movie["imdb_id"]})
    data = doc[0]
    data = data["info_recommended"]
    return data

    