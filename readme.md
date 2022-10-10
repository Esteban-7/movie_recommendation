# Movie recommendation 

The general idea of our project was to create our own  movie recommendation system from the IMDB site. 


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Getting-started ">Getting started</a>
      <ul>
        <li><a href="#steps">Steps</a></li>
      </ul>
    </li>
    <li>
      <a href="#search-movie">Search movie</a>
    </li>
    <li><a href="#Get-movie-information">Get movie information</a></li>
    <li><a href="#Get-movie-recommendation">Get movie recommendation </a></li>
    <li><a href="#IMDB-scraper ">IMDB scrapper</a></li>
    <li><a href="#Storing-data-into-MongoDB">Storing data into MongoDB</a></li>
    <li><a href="#Creating-a-movie-recommendation">Creating a movie recommendation system </a></li>
    <li><a href="#Data-analysis-and-Dashboard">Data analysis and Dashboard </a></li>
    <li><a href="#all_together">All together </a></li>
  </ol>
</details>




## Getting Started

For this, we divided our work in several parts, each  connected to the rest that we will see below. 
***First of all, we decided to use the recommendation from IMDB diagram. We  used all three selenium, beautiful soup and scrapy to collect all the information we needed from the site. The data  we scraped  from each film is then saved in a Mongodb database. Then, we start building our recommendation system by estimating distance between movies. Finally, to show our work, we created dashboards to do some data analysis comparing IMDB recommendation system and our own.


### Steps

A step by step guide that shows you how to get the development environment up and running.

```

$ search_movies.py
$ movie_info.py
$ imdb_recommendations.py
$ imdb_mongo.py
$ imdb_scraper.py
$ movie_distance.py
$ stream_show.py 
$ imdb_main.py
$ run.py

```

## Search movie 
* Using Selenium


We create a function that asks the user for the input of the name of the movie and it searches the name in imdb search service.
Selenium webdriver is used to access to the imdb search service.
The function takes as argument the path to search for the executable webdriver. The path is given from the main module where this function is called.
We use it to find the tables that hold the search results and create a dictionary.
As a result, the function returns the direct link of the movie the user wanted to search and the movie id in the imdb database.



## Get movie information 
* Using Beautiful Soup

In this part we create several functions to scrap the information of a given movie but it's id in imdb.
The scraping here includes the request to the imdb webpage of a given movie and then getting the information from it using Beautiful Soup.
We gather the most basic information such as: name, budget, earnings, genres, cast, directors and imdb rating using only the home page of the movie. Next,using the movie id, we collect info such as year release of the movie, runtime in minutes for a given  movie, number of votes in the imdb platform for a given movie, the metascore rating of a given movie, the number of reviews by users in the imdb platform for a given movie,the number of critics reviews on external websites to imdb but gathered by imdb for a given movie.
After collecting all the data we needed, we use all defined functions before in order to create a dictionary object called movie, in which the information for a given movie id is held.
(#takes as argument a movie and the type of recommendation (imdb or our own) to get the information of all recommended movies. )
 

## Get movie recommendations
* Using Beautiful Soup

To get the recommendations from imbd site we continue using beautiful soup.
We created a function that requests the url and gets the hrefs for the movies recommended in the "more like this" section in imdb page for a movie. This function returns a list of hrefs elements that link to the movies recommended by imdb.
Then we create another function containing the id of the movie and the depth of diagram which searches in the IMDB "more like this" for recommendations based on the link of one movie. We have to give as :

* Input: IMDB link to a movie/show. 
* Depth: amount of iterations to search in the "more like this"
* Output: a list of links for imdb movies/shows. 

***Now that we have the movies id recommended by imdb we go back into movie_info where we create a function which takes as argument a movie and the type of recommendation (imdb or our own) to get the information of all recommended movies. 


## IMDB scraper
 * Using Scrapy
 
We use scrapy to collect the id of the movie and to get from one page to the next one....



## Storing data into MongoDB
* Using info_recommendations from movie_info


Create a function into movie_info that takes as argument a movie and the type of recommendation (imdb or our own) to get the information of all recommended movies.
We create another function to save a given movie object in the "movie" collection in MongoDB database. Moreover, we need to upload  the information of the recommended movies into mongodb.
Finally, we get a movie (dictionary of info),  which returns the list of dictionaries for all the movies recommended by imdb that were saved in the mongodb.

## Creating a movie recommendation system
* Using distance


To create our own recomendation system we need to use distance package.
We create a function which takes two lists and estimates how similar the second list is to the first one. The result might be between 0 and 1.
Then, we estimate the movie distance by given two movie objects (dictionaries).
Furthermore, the lists of cast, directors and genres are transformed comparing the elements of both movies and estimating the common elements rate.
Since all  the data is numeric,  we calculate euclidean and manhattan distances.

## Data Analysis and Dashboard
* Using streamlit, plotly, json , pandas 

For this last part, we created  and displayed a dashboard containing the recommended movies.
The script reads the imdb_id_movie json file created in which the id of the movie in study is saved. Then reads the recommendation collection in the mongoDB database.
From the information gathered with mongodb, the dataframes using the imdb recommendations and our recommendations are created. From them, different plots are designed with plotly.
To display the plots we use streamlit. 
Finally we can compare both recommendation systems.


## All  together 
All in all,  we create a new function called new_movie used to find  the link and ID to the imdb page of a movie by searching for it using the search movies module (selenium module)
Given the ID of the chosen movie, a new movie object is created using the movie_info module, gathering the features of the film with beautiful soup.
We need to call the get_imdb_recommendations module, which scraps the webpage of a film to gather the "more like this" recommendations by imdb's system
After that, we call on the scrap_imdb and passes the genres of the movie as the argument. Creating a long list of movies with the same set of genres.
To make the script run, we create a movie element and it uploads its information, as well as the recommendations information to the mongoDB database
This will generates a temp file called imdb_movie_id in which the id of the film is saved for it to be read later by the streamlit module.
Finally to make everything run, we call the imdb_main module on our terminal and also call the streamlit module.
* the imdb_main module : handles the creation of a movie, filling its information and calling the methods to scrap the recommended films.
* the stream_show module : handles the movie saved in mongoDB and generates the dashboard with the plots to study. 




