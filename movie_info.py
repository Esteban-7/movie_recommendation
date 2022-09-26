import requests 
from bs4 import BeautifulSoup
import re # regex expression
import tqdm.notebook as tq # time loop in notebook
import re

def get_year(movie_id):
    url = "https://www.imdb.com/title/"+movie_id+ "/releaseinfo?ref_=tt_ov_rdat"
    
    print(url)
    try:
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
        year = soup.find("td", attrs = {"class" : "release-date-item__date"}).getText()
        year = int(year.split(" ")[2]) #split the date by whitespaces. Get the third element, which is the year of release.
        
        return year
    except:
        print("Date not available")
        return 0

def get_runtime(movie_id):
    url = "https://www.imdb.com/title/"+movie_id+ "/technical?ref_=tt_spec_sm"
    
    print(url)
    try:
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
        
        table = soup.find("table", attrs = {"class" : "dataTable labelValueTable"}).find("tbody")
        
        children = table.contents
        runtime = children[1].contents[3].getText().split("(")[1]
        runtime = runtime.split(" ")[0]
        
        return runtime
    
    except:
        print("Runtime not available")
        return 0

def get_votes(movie_id):
    url = "https://www.imdb.com/title/"+movie_id+ "/ratings/"
    
    print(url)
    try:
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
        
        votes = soup.find("td", attrs = {"class" : "ratingTable Selected"}).find("div", attrs = {"class":"smallcell"}).getText()
        votes = re.sub("[^0-9]", "", votes)
        return int(votes)
    
    except:
        print("Votes not available")
        return 0
    
def get_metascore(movie_id):
    url = "https://www.imdb.com/title/"+movie_id+ "/criticreviews/"
    
    print(url)
    try:
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
        
        metascore = soup.find("div", attrs = {"class" : "metascore_block"}).find("div", attrs = {"class":"metascore_wrap"})
        metascore = metascore.find("span").getText()
        
        return int(metascore)
    
    except:
        print("Metascore not available")
        return 0

def get_num_reviews(movie_id):
    url = "https://www.imdb.com/title/"+movie_id+ "/reviews/"
    
    print(url)
    try:
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
        
        num_reviews = soup.find("div", attrs = {"class" : "lister"}).find("div", attrs = {"class":"header"})
        num_reviews = num_reviews.find("span").getText()
        num_reviews = re.sub("[^0-9]", "", num_reviews)
        return int(num_reviews)
    
    except:
        print("Number of reviews not available")
        return 0

def get_num_exernal_reviews(movie_id):
    url = "https://www.imdb.com/title/"+movie_id+ "/externalreviews/"
    
    print(url)
    try:
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
        
        num_reviews_external = soup.find("div", attrs = {"id" : "external_reviews_content"}).find("div", attrs = {"class":"nav"}).getText()
        num_reviews_external = re.sub("[^0-9]", "", num_reviews_external)
        return int(num_reviews_external)
    
    except:
        print("Number of external reviews not available")
        return 0


def get_movie_info(movie_id):
    movie = {"name": "--",
          "imdb_id": movie_id,
         "year_released": get_year(movie_id),
         "runtime": get_runtime(movie_id),
          "imdb_reviews": get_num_reviews(movie_id),
         "external_reviews": get_num_exernal_reviews(movie_id),
         "imdb_rating": 8.7,
         "metacritic_punctuation": get_metascore(movie_id),
          "budget": 00000,
          "earning_worldwide": 00000,
          "earning_US&CA": 00000,
          "genres": ["----"],
          "directors":["----"],
          "cast":["----"] #,
          #"imdb_recommendations": {},
          #"new_recommendations": {}
         } 
    return movie

print(get_movie_info("tt1707386"))

