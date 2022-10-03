from concurrent.futures import process
from gc import callbacks
from webbrowser import get
import scrapy
from scrapy.crawler import CrawlerProcess

class imdbSpider(scrapy.Spider):
    name = "imdbSpider"
    start_urls = ["https://www.imdb.com/search/title/?title_type=movie&genres=drama&sort=num_votes,desc"]
    movies = []


    def parse(self, response):
        
        while len(self.movies)< 500:
            for movie in response.css("div.lister-item-content"):
                movie = movie.css("a").attrib["href"]
                movie = movie.split("title/")[1]
                self.movies.append(movie)
                 
            next_page = response.css("a.lister-page-next.next-page").attrib["href"]

            if next_page is not None:
                yield response.follow(next_page, callback = self.parse)

        yield {"recommended": self.movies}



def scrap_imdb():    
    process = CrawlerProcess(settings={
    "FEEDS": {
        "recommended.json": {"format": "json"},
    },
})
    process.crawl(imdbSpider)
    process.start()

scrap_imdb()
