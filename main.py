from search_movie.search_movie import search_movies
from os import getcwd


path = getcwd() + "\driver\chromedriver"
print(path)

x = search_movies(path)
print(x)
