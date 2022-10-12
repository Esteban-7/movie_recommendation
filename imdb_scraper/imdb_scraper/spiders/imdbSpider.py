from concurrent.futures import process
from gc import callbacks
from webbrowser import get
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import re

class imdbSpider(scrapy.Spider):
    #Creates a spider class to scrap the recommended movies according to the genres of a given movie
    name = "imdbSpider"
    start_urls = []
    movies = []

    def __init__(self, genres= []):
        #in the constructor function a list of genres must be passed, the genres of the movie modify the search of the recommended movies
        #so the list of the genres is important to get the link to scrap
        genres_string = ","
        genres_string = genres_string.join(genres)
        start_url = "https://www.imdb.com/search/title/?title_type=movie&genres=" + genres_string + "&sort=num_votes,desc&explore=title_type,genres"
        self.start_urls.append(start_url) 
        self.max_movies = int(input("Max number of movies Scrapped for new recommendations: "))


    def parse(self, response):
        #in the parse function the starting irl is scraped, the name and ids for the first 500 the movies recommended by the imdb by the genres selected are taken
        # a temporal file is created with the information of all 500 movies recommmended. so that it later can be saved by the imdb_mongo module
        
        for movie in response.css("div.lister-item-content"):
            movie = movie.css("a").attrib["href"]
            movie = movie.split("title/")[1]
            movie = re.sub("/","",movie)
            self.movies.append(movie)
            
            if len(self.movies) > self.max_movies:
                break
            
 
        next_page = response.css("a.lister-page-next.next-page").attrib["href"]

        if (next_page is not None) and (len(self.movies)<self.max_movies):
                yield response.follow(next_page, callback = self.parse)
        
        with open('imdb_scraper/imdb_scraper/spiders/recommended.json', 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
        



def scrap_imdb(genres = []):    
    #generates a crawler process so that the spider created can be called from a python script. The funtion takes as arguments a list of genres 
    #which in turn is used to create an instance of the spider.
    try:
        process = CrawlerProcess()
        process.crawl(imdbSpider, genres = genres)
        process.start()
        return True
    except:
        print("Unexpected error in Scrapy Module -- Est. Ort.")
        return False
        

