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
    <li><a href="#Data-analysis-and-Dashboard">Data analysis and Dashboard </a></li>
    <li><a href="#Creating-a-movie-recommendation">Creating a movie recommendation system </a></li>
    <li><a href="#all_together">All together </a></li>
    <li><a href="#difficulties_on_development">Difficulties on development </a></li>
  </ol>
</details>




## Getting Started

For this, we divided our work into several modules, each connected to the rest that we will explain below. 
First of all, we interact with the "More like this" function on the IMDb platform to generate a list of recommendations based on a film. We  use selenium, beautiful soup and scrapy to collect all the information we needed from the site. The data  we scrap  from each film is then saved in a Mongodb database. Then, we propose our recommendation system by finding a list of movies based on the genre of a given movie, then estimating distance between movies and choosing the closest . Finally, to show the results, we created dashboards to do some data analysis comparing IMDB recommendation system and our own.

### Requirements:

The installation of the following packages is required:
- Beautiful Soup
- Scrapy
- Selenium
- Plotly
- Streamlit
- Scypy
- Pandas
- json

In addition, it is necessary to download the proper driver for Chrome browser according to the user OS.
The installation of mongoDB is also required for the program to run, the configuration for the collections used must be updated in the imdb_mongo module. 


### Modules

A guide that shows how the development environment is set up and run.

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
We use it to find the tables that hold the search results and create a dictionary of the different movies as result of the search.
As a result, the function returns the direct link of the movie the user wanted to search and the movie id in the imdb database.



## Get movie information 
* Using Beautiful Soup

In this module we create several functions to scrap the information of a given movie by it's id in imdb.
The scraping here includes the request to the imdb webpage of a given movie and then getting the information from it using Beautiful Soup.
We gather the most basic information such as: name, budget, earnings, genres, cast, directors and imdb rating using only the home page of the movie. Next,using the movie id, we collect info such as year release of the movie, runtime in minutes for a given  movie, number of votes in the imdb platform for a given movie, the metascore rating of a given movie, the number of reviews by users in the imdb platform for a given movie,the number of critics reviews on external websites to imdb but gathered by imdb for a given movie.
After collecting all the data we needed, we use all defined functions before in order to create a dictionary object called movie, in which the information for a given movie id is held.
(#takes as argument a movie)
 

## Get movie recommendations
* Using Beautiful Soup

To get the recommendations from imbd site we continue using beautiful soup.
We created a function that requests the url and gets the hrefs for the movies recommended in the "more like this" section in imdb page for a movie. This function returns a list of hrefs elements that link to the movies recommended by imdb.
Then we create another function containing the id of the movie and the depth of the research for recommendations which searches in the IMDB "more like this" for recommendations based on the link of one movie. We have to give as :

* Input: IMDB link to a movie/show. 
* Depth: amount of iterations to search in the "more like this"
* Output: a list of links for imdb movies/shows. 



## IMDB scraper
 * Using Scrapy
 
Given the list of genres for a movie, a search on IMDb platform can be held to see all movies containing such genres, from there, the list can be arranged by the number of votes. We use this list to gather information about related movies for our own recommendation system. Since there can be thousands of movies with the same genres, the Scrapy package is used to browse on the results page and gather all the id's of the related movies. This part of the module gets as an argument the max number of movies that the user wants to include for the recommendation. With the list of Id's, the beautiful soup module is used again to gather all details of each movie in the list. 


## Creating a movie recommendation system
* Using distance


To create our own recomendation system we need to use distance package.
First we create a function which takes two lists and estimates how similar the second list is to the first one. The result might be between 0 and 1. This is made to compare the list of genres, actors and directors for two different movies. The lists of cast, directors and genres are transformed comparing the elements of both movies and estimating the common elements rate.
Then, we estimate the movie distance by given two movie objects (dictionaries).
Since all  the data is numeric,  we calculate euclidean and manhattan distances. The recommended movies will be the ones that, out of the movies with the same genre as the original one, have the shortest distance to the latter. 


## Storing data into MongoDB
* Using info_recommendations from movie_info


We create another function to save a given movie object in the "movie" collection in MongoDB database. Moreover, we need to upload  the information of the recommended movies into mongodb.
Finally, we get a movie (dictionary of info),  which returns the list of dictionaries for all the movies recommended by imdb that were saved in the mongodb. For the information to be read later. 


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



## Difficulties on development

1. Changing of IMDb UI for results page: after Selenium can manage to search for a movie using the search bar, two different UI's can appear showing the results, this is caused by an update on the app that they might be testing at the moment. Given that the user cannot control which version of the app is going to get, a try/except piece of code had to be implemented to handle both versions. 
2. After gather all the id's from movies with the same genres as the initial movie, it gets time consuming to scrap all details needed from each movie in order to get the distance to the original movie. For this reason, this part of the script is handled with parallelization, so the process is more time efficient.
3. For the scrapy module to work, it is necessary to call the python interpreter, however, to make it part of all the code, a solution was to call the crawler process inside a function, so that the spider can be called from within a python script. 
4. To correctly use the streamlit module it is necessary to call on the terminal the "streamlit run" command. However, for the imdb_main module, it is necessary to call the python interpreter so that the scrapy module doesn't show any error. For this, the "run" module is designed, so that both the python and the streamlit commands can be called from the terminal by using the "os" package. 
5. For the dashboard module, in the plotly plots an error showed in which the distribution of the euclidean or manhattan distance cannot be estimated given that some observations have non finite value. This can be avoided by not including in the analysis movies that are not out yet (pre production) and movies that are not the intial movie for the recommendations. 

