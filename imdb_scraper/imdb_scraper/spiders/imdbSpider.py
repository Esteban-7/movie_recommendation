from concurrent.futures import process
from gc import callbacks
from webbrowser import get
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import re

class imdbSpider(scrapy.Spider):
    name = "imdbSpider"
    start_urls = []
    movies = []

    def __init__(self, genres= []):
        genres_string = ","
        genres_string = genres_string.join(genres)
        start_url = "https://www.imdb.com/search/title/?title_type=movie&genres=" + genres_string + "&sort=num_votes,desc&explore=title_type,genres"
        self.start_urls.append(start_url) 


    def parse(self, response):
        
        for movie in response.css("div.lister-item-content"):
            movie = movie.css("a").attrib["href"]
            movie = movie.split("title/")[1]
            movie = re.sub("/","",movie)
            self.movies.append(movie)
            
            if len(self.movies) > 500:
                break
            
 
        next_page = response.css("a.lister-page-next.next-page").attrib["href"]

        if (next_page is not None) and (len(self.movies)<500):
                yield response.follow(next_page, callback = self.parse)
        
        with open('imdb_scraper/imdb_scraper/spiders/recommended.json', 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
        



def scrap_imdb(genres = []):    
    try:
        process = CrawlerProcess()
        process.crawl(imdbSpider, genres = genres)
        process.start()
        return True
    except:
        print("Unexpected error in Scrapy Module -- Est. Ort.")
        return False
        

