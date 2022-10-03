import requests 
from bs4 import BeautifulSoup
import re # regex expression
import tqdm.notebook as tq # time loop in notebook
import re
from movie_distance import estimateMovieDistance


def get_title(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    try:
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
    
        title = soup.find('h1', attrs = {"data-testid" : "hero-title-block__title"}).getText()
    
        return title
    except:
        print("Title is not available")
        return 0

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
        runtime = int(runtime)
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

def get_budget(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    try:

        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')

        budget = soup.find('li', attrs = {"data-testid":'title-boxoffice-budget'}).find('span', class_ 
                                                                        ='ipc-metadata-list-item__list-content-item').getText()
    
        import re
        budget = re.sub("[^0-9]", "", budget)
        return int(budget)

    except:
        print("Budget is not available")
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

def get_gross_Worldwide(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    
    try:

        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')

        gross_Worldwide = soup.find('li', attrs = {"data-testid":'title-boxoffice-cumulativeworldwidegross'}).find('span', class_ = 'ipc-metadata-list-item__list-content-item').getText()

        import re
        gross_Worldwide = re.sub("[^0-9]", "",gross_Worldwide)
        return int(gross_Worldwide)
    except:
        print("Gross Worldwide is not available")
        return 0

def get_gross_Canada_US(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    
    try:
        
        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')

        gross_US_et_Canada = soup.find('li', attrs = {"data-testid":'title-boxoffice-grossdomestic'}).find('span', class_ = 'ipc-metadata-list-item__list-content-item').getText()
    
        import re
        gross_US_et_Canada = re.sub("[^0-9]", "", gross_US_et_Canada)
        return int(gross_US_et_Canada)

    except:
        print("Gross Canada et US is not available")
        return 0

def get_genre(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    try:

        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
    
        genre = soup.find('div', class_ = 'ipc-chip-list__scroller').find_all('a', class_ = 'sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')

        genres = []

        for i in genre:
            x = i.getText()
            genres.append(x)
    
        return genres
    except:
        print("Genre is not available")
        return [0]

def get_top_cast(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    try:

        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
    
        top_cast = soup.find('div', class_ = 'ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid').find_all('a',class_ = 'sc-36c36dd0-1 QSQgP')

        top_casts = []

        for i in top_cast:
            b = i.getText()
            top_casts.append(b)

        return top_casts
    except:
        print("Top cast is not available")
        return [0]

def get_director(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    try:

        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')
    
        director = soup.find('li', class_ = 'ipc-metadata-list__item').find_all('a', class_ = 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')

        directors = []

        for i in director:
            y = i.getText()
            directors.append(y)

        return directors
    except:
        print("Director is not available")
        return [0]

def get_rating(movie_id):
    url = "https://www.imdb.com/title/"+movie_id
    
    print(url)
    
    try:

        response = requests.get(url)
        result = response.content    
        soup = BeautifulSoup(result, 'html.parser')

        rating = soup.find('div',  attrs = {"data-testid":'hero-rating-bar__aggregate-rating__score'}).find('span', class_ = 'sc-7ab21ed2-1 jGRxWM').getText()
        rating = float(rating)    

        return rating
    except:
        print("Rating is not available")
        return 0


def get_movie_info(movie_id):
    movie = {"name": get_title(movie_id),
          "imdb_id": movie_id,
         "year_released": get_year(movie_id),
         "runtime": get_runtime(movie_id),
          "imdb_reviews": get_num_reviews(movie_id),
         "external_reviews": get_num_exernal_reviews(movie_id),
         "imdb_rating": get_rating(movie_id),
         "metacritic_punctuation": get_metascore(movie_id),
          "budget": get_budget(movie_id),
          "earning_worldwide": get_gross_Worldwide(movie_id),
          "earning_US&CA": get_gross_Canada_US(movie_id),
          "genres": get_genre(movie_id),
          "directors":get_director(movie_id),
          "cast":get_top_cast(movie_id) #,
          #"imdb_recommendations": {},
          #"new_recommendations": {}
         } 
    return movie





def info_recommendations(movie1,type_recommendation):
    #takes as argument a movie and the type of recommendation (imdb or our own) to get the information of all recommended movies. 
    if type_recommendation == "imdb":
        array = movie1["imdb_recommendations"]
    else:
        array = movie1["new_recommendations"]

    movies = []
    for movie_id in array:
        movie = get_movie_info(movie_id)
        movie["euclidean_distance"] = estimateMovieDistance(movie1,movie)[0]
        movie["manhattan_distance"] = estimateMovieDistance(movie1,movie)[1]
        movies.append(movie)
    return movies
