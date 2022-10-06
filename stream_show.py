from turtle import color, title
import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
import pymongo
import json
#from imdb_main import recommend


def stream_imdb():

    client = pymongo.MongoClient("localhost",27017)
    db = client["movie_recommendations"]
    collection = db["movie_recommendation"]
    with open("imdb_id_movie.json","r") as f:
        imdb_movie_id = json.load(f)["imdb_movie_id"]
    
    doc = collection.find({"movie_id": imdb_movie_id})

    recommended = doc[0]


    column_names = {"name": "Name", "year_released": "Year", "imdb_reviews":"IMDb reviews",
                    "external_reviews": "External Reviews", "imdb_rating":"IMDb Rating",
                    "metacritic_rating": "Metacritic Rating","euclidean_distance": "Euclidean Distance"}

    movie_name = recommended["movie_name"]
    imdb_df = pd.DataFrame(recommended["imdb_recommended"])
    imdb_df["type"] = "imdb_recommended"
    imdb_df = imdb_df.loc[imdb_df["imdb_id"] != imdb_movie_id]
    imdb_df = imdb_df.loc[imdb_df["imdb_rating"] != 0]
    genres_imdb = list(imdb_df["genres"])
    directors_imdb = list(imdb_df["directors"])
    cast_imdb = list(imdb_df["cast"])

    new_df = pd.DataFrame(recommended["new_recommended"])
    new_df = new_df.loc[new_df["imdb_id"] != imdb_movie_id] 
    new_df = new_df.sort_values(by = ["euclidean_distance"])
    new_df = new_df[:len(imdb_df)]
    new_df = new_df.reset_index()
    new_df["type"] = "new_recommended"
    genres_new = list(new_df["genres"])
    directors_new = list(new_df["directors"])
    cast_new = list(new_df["cast"])

    total_df = pd.concat([imdb_df,new_df], axis=0) 
    total_df = total_df.drop(["genres","directors","cast","index"], axis = 1).reset_index()

    cols_to_norm = ['euclidean_distance','manhattan_distance']
    total_df[['euclidean_distance_normalized','manhattan_distance_normalized']] = total_df[cols_to_norm].apply(lambda x: (x) / (x.max()))
    imdb_df = total_df.loc[total_df["type"] =="imdb_recommended"]
    new_df = total_df.loc[total_df["type"] =="new_recommended"]
    new_df = new_df.reset_index()

    st.title("Movie Recommendation System!")
    st.header(f"IMDb recommended Movies based on {movie_name}:")
    st.write(f""" Average IMDb rating : {round(imdb_df["imdb_rating"].mean(),2)} (range: {imdb_df["imdb_rating"].min()}-{imdb_df["imdb_rating"].max()})\n
    Average number of IMDB reviews: {round(imdb_df["imdb_reviews"].mean())} (range: {imdb_df["imdb_reviews"].min()}-{imdb_df["imdb_reviews"].max()})\n
    Average number of external reviews: {round(imdb_df["external_reviews"].mean() )} (range: {imdb_df["external_reviews"].min()}-{imdb_df["external_reviews"].max()})\n
    Average Metacritic rating : {round(imdb_df["metacritic_rating"].mean())} (range: {imdb_df["metacritic_rating"].min()}-{imdb_df["metacritic_rating"].max()})
    """)
    st.dataframe(imdb_df[["name","year_released","imdb_reviews","external_reviews","imdb_rating","metacritic_rating","euclidean_distance","euclidean_distance_normalized","manhattan_distance","manhattan_distance_normalized"]].rename(columns= column_names))


    st.header(f"Our recommended Movies based on {movie_name}:")
    st.write(f""" Average Imdb rating : {round(new_df["imdb_rating"].mean(),2)} (range: {new_df["imdb_rating"].min()}-{new_df["imdb_rating"].max()})\n
    Average number of IMDB reviews: {round(new_df["imdb_reviews"].mean())} (range: {new_df["imdb_reviews"].min()}-{new_df["imdb_reviews"].max()})\n
    Average number of external reviews: {round(new_df["external_reviews"].mean() )} (range: {new_df["external_reviews"].min()}-{new_df["external_reviews"].max()})\n
    Average Metacritic rating : {round(new_df["metacritic_rating"].mean())} (range: {new_df["metacritic_rating"].min()}-{new_df["metacritic_rating"].max()})
    """)
    st.dataframe(new_df[["name","year_released","imdb_reviews","external_reviews","imdb_rating","metacritic_rating","euclidean_distance","euclidean_distance_normalized","manhattan_distance","manhattan_distance_normalized"]].rename(columns= column_names))

    # Aggregated distances
    st.header("Aggregated distances per type of recommendation")
    st.write(f"The total Euclidean distance for our recommendations is {round(new_df.euclidean_distance.sum() / imdb_df.euclidean_distance.sum() * 100 )}% of that of the IMDb recommendations.")
    distance_euclidean = px.histogram(total_df, x='type', y='euclidean_distance', labels = {"type":"Type of Recommendation","euclidean_distance": "Euclidean Distance"})
    distance_euclidean.update_layout(title_text="Euclidean Distance:")
    st.plotly_chart(distance_euclidean, use_container_width=False)

    st.write(f"The total Manhattan distance for our recommendations is {round(new_df.manhattan_distance.sum() / imdb_df.manhattan_distance.sum() * 100 )}% of that of the IMDb recommendations.")
    distance_manhattan = px.histogram(total_df, x='type', y='manhattan_distance', labels = {"type":"Type of Recommendation","manhattan_distance": "Manhattan Distance"})
    distance_manhattan.update_layout(title_text="Manhattan Distance:")
    st.plotly_chart(distance_manhattan, use_container_width=False)

    #Distribution of Euclidean Distance
    st.write("Distribution for Euclidean Distances:")
    distribution_euclidean = ff.create_distplot([imdb_df["euclidean_distance_normalized"],new_df["euclidean_distance_normalized"]],
                                                        group_labels=["imdb_recommended","new_recommended"],
                                                        bin_size=0.07,curve_type="normal", show_rug=False)

    st.plotly_chart(distribution_euclidean, use_container_width=True)

    st.write("Distribution for Manhattan Distances:")
    distribution_manhattan = ff.create_distplot([imdb_df["manhattan_distance_normalized"],new_df["manhattan_distance_normalized"]],
                                                        group_labels=["imdb_recommended","new_recommended"], 
                                                        bin_size=0.07,curve_type="normal", show_rug=False)

    st.plotly_chart(distribution_manhattan, use_container_width=True)

    # Ratings distribution
    st.header("Ratings per type of recommendation")
    st.write("Distribution for the IMDb rating:")
    distribution_imdb_rating = ff.create_distplot([imdb_df["imdb_rating"],new_df["imdb_rating"]], group_labels=["imdb_recommended","new_recommended"], bin_size=0.5,curve_type="normal",show_rug=False)
    st.plotly_chart(distribution_imdb_rating, use_container_width=False)

    st.write("Distribution for the Metacritic rating:")
    distribution_metacritic_rating = ff.create_distplot([imdb_df["metacritic_rating"],new_df["metacritic_rating"]], group_labels=["imdb_recommended","new_recommended"], bin_size=10,curve_type="normal",show_rug=False)
    st.plotly_chart(distribution_metacritic_rating, use_container_width=False)


    distance_rating_euclidean = px.scatter(total_df, x = "imdb_rating", y ="euclidean_distance", color = "type", labels= {"imdb_rating": "IMDb Rating","euclidean_distance":"Euclidean Distance", "type": "Type of Recommendation"})
    distance_rating_euclidean.update_layout(title_text = "Relationship between the IMDb rating and the distance (Euclidean):")
    st.plotly_chart(distance_rating_euclidean, use_container_width=True)

    distance_rating_manhattan = px.scatter(total_df, x = "imdb_rating", y ="manhattan_distance", color = "type", labels= {"imdb_rating": "IMDb Rating","manhattan_distance":"Manhattan Distance", "type": "Type of Recommendation"})
    distance_rating_manhattan.update_layout(title_text = "Relationship between the IMDb rating and the distance (Manhattan):")
    st.plotly_chart(distance_rating_manhattan, use_container_width=True)

    # Interesting questions
    st.header("Interesting questions about the movies...")
    #DO THE RECOMMENDED MOVIES GET BETTER WITH TIME
    st.subheader("Do movies get better with Time?")
    time_rating_imdb = px.scatter(total_df.loc[total_df["year_released"] != 0], x = "year_released", y ="imdb_rating", color= "type",
                                labels  = {"year_released": "Year of release","imdb_rating": "IMDb Rating", "type": "Type of recommendation"})
    time_rating_imdb.update_layout(title_text = "Relationship between the IMDb rating and year of release")
    st.plotly_chart(time_rating_imdb)

    time_rating_metacritic = px.scatter(total_df.loc[total_df["year_released"] != 0], x = "year_released", y ="metacritic_rating", color= "type",
                                labels  = {"year_released": "Year of release","metacritic_rating": "Metacritic Rating", "type": "Type of recommendation"})
    time_rating_metacritic.update_layout(title_text = "Relationship between the Metacritic rating and year of release")
    st.plotly_chart(time_rating_metacritic)
    #DO THE RECOMMENDED MOVIES GET BETTER WITH BUDGET
    st.subheader("Do movies get better with more budget?")
    budget_rating_imdb = px.scatter(total_df.loc[total_df["budget"] != 0], x = "budget", y ="imdb_rating", color= "type",
                                labels  = {"budget": "Budget","imdb_rating": "IMDb Rating", "type": "Type of recommendation"})
    budget_rating_imdb.update_layout(title_text = "Relationship between the IMDb rating and Budget")
    st.plotly_chart(budget_rating_imdb)

    budget_rating_metacritic = px.scatter(total_df.loc[total_df["budget"] != 0], x = "budget", y ="metacritic_rating", color= "type",
                                labels  = {"budget": "Budget","metacritic_rating": "Metacritic Rating", "type": "Type of recommendation"})
    budget_rating_metacritic.update_layout(title_text = "Relationship between the Metacritic rating and Budget")
    st.plotly_chart(budget_rating_metacritic)

    #earnings and quality
    st.subheader("Do good movies earn more?")
    earning_worldwide_imdb = px.scatter(total_df.loc[total_df["imdb_rating"] != 0], x = "imdb_rating", y ="earning_worldwide", color= "type",
                                labels  = {"earning_worldwide": "Earnings Worldwide","imdb_rating": "IMDb Rating", "type": "Type of recommendation"})
    earning_worldwide_imdb.update_layout(title_text = "Relationship between the IMDb rating and Worldwide earnings")
    st.plotly_chart(earning_worldwide_imdb)

    earning_worldwide_metacritic = px.scatter(total_df.loc[total_df["metacritic_rating"] != 0], x = "metacritic_rating", y ="earning_worldwide", color= "type",
                                labels  = {"earning_worldwide": "Earnings Worldwide","metacritic_rating": "Metacritic Rating", "type": "Type of recommendation"})
    earning_worldwide_metacritic.update_layout(title_text = "Relationship between the Metacritic rating and Worldwide earning")
    st.plotly_chart(earning_worldwide_metacritic)

    #critics and users
    st.subheader("Are users in line with critics?")
    imdb_metascore = px.scatter(total_df.loc[total_df["imdb_rating"] != 0], x = "imdb_rating", y ="metacritic_rating", color= "type",
                                labels  = {"metacritic_rating": "Metacriti Rating","imdb_rating": "IMDb Rating", "type": "Type of recommendation"})
    imdb_metascore.update_layout(title_text = "Relationship between the IMDb rating and Metacritics Rating")
    st.plotly_chart(imdb_metascore)


stream_imdb()