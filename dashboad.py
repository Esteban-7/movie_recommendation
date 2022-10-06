import streamlit as st
import pandas as pd

movies = {}
for i in range(1,70):
    movie = {"name": "Film__" + str(i),
              "imdb_id": str(i),
             "year_released": 2000 + i,
             "runtime": 100+i,
              "imdb_reviews": 400+i,
             "external_reviews": 50+i,
             "imdb_rating": i/(i+1),
             "metacritic_punctuation": (i+10)/(i+1),
              "budget": 1000+i,
              "earning_worldwide": 500*i,
              "earning_US&CA": 50*i,
              "genres": ["action","sci-fi","drama","romance"],
              "directors":[f"Director1_{str(i)}",f"Director2_{str(i)}"],
              "cast":[f"Actor_{str(i)}", f"Actor_{str(i)+str(i)}",f"Actor_{str(i)+str(i)+str(i)}"],
              "imdb_recommendations": {},
              "new_recommendations": {}
             }
    movies[i] = movie

df=pd.DataFrame.from_dict(movies, orient='index')
df.drop(["genres", "directors","cast","imdb_recommendations","new_recommendations"], axis = 1, inplace = True,errors='ignore')
df
st.dataframe(df)