import requests 
from bs4 import BeautifulSoup
import re # regex expression



def Get_hrefs(url):
    # Request url and gets the hrefs for the movies recommended in the "more like this" section in imdb page for a movie.
    # Returns a list of hrefs elements that link to the movies recommended by imdb
    
    response = requests.get(url)
    result = response.content    
    soup = BeautifulSoup(result, 'html.parser')
    
    # init the list with all href
    hrefs = []
    
    for poster in soup.find_all("div",attrs={'class':'ipc-poster-card ipc-poster-card--base ipc-poster-card--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2'}):
        for link in poster.find_all("a", attrs = {"class":"ipc-lockup-overlay ipc-focusable"}):
            if "href" in link.attrs:
                if link.get("href") not in hrefs:
                    movie_id = link.get("href").split("/?")[0] #only the first part of the link is required as it contains the id of the film. The next sequence might cause errors. 
                    hrefs.append(movie_id) #save the links (ids) in a list.
    return(hrefs)

def get_imdb_recommendations(movie_id,depth):
    #Searches in the IMDB "more like this" for recommendations based on the link of one movie. 
    #Input: IMDB link to a movie/show. Depth: amount of iterations to search in the "more like this"
    #Output: a list of links for imdb movies/shows. 
    url = "https://www.imdb.com/title/" + movie_id
    
    urls_checked = []

    for i in range(depth):
        if i == 0:
            
            hrefs  = Get_hrefs(url)
            urls_checked.append(url) 
        else:
            hrefs_temp = []
            for href in hrefs:
                new_url = "https://www.imdb.com" + href
                if new_url not in urls_checked:
                    hrefs_temp += Get_hrefs(new_url)
                    urls_checked.append(new_url)
                    hrefs_temp = list(set(hrefs_temp))
            hrefs += [recom for recom in hrefs_temp if recom not in hrefs]
    
    movies_id = [i.split("title/")[1] for i in hrefs]
    
    return movies_id

