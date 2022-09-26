from selenium import webdriver
from os import getcwd


def search_movies(path):

    # This function asks the user for the input of the name of the movie. Searches the name of the movie in imdb search service.
    # Selenium webdriver is used to access to the imdb search service.
    # The function takes as argument the path to search for the executable webdriver. Path is given from the main module where this function is called. 
    # As a result the function returns the direct link of the movie the user wanted to search and the movie id in the imdb database. 
    
    search= input('Search movies:') #name of the movie from user
    website = 'https://www.imdb.com/'
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #options to avoid abnormal logging
    
    driver = webdriver.Chrome(path,options=options)
    
    driver.get(website)
    driver.find_element("id",'suggestion-search').send_keys(search)
    driver.find_element("id", 'suggestion-search-button').click()
    
    #find the tables that hold the results of the search. 
    table=driver.find_element("xpath",'//*[@id="main"]/div/div[2]/table')
    
    
    results_search = table.find_elements("class name", "result_text")
    results = []
    for result in results_search:
        results += result.find_elements("tag name","a") #get the elements results of the search
    
    options = {}
    for i in range(len(results)):
        row = results[i]
        option = i+1
        name=row.text
        href = row.get_attribute('href')    
        options[option] = {"name": name,"href": href} #create a dictionary with the results of the search
    
    for option in options.keys():
        print(option, " ","name: ", options[option]["name"], "  link:",options[option]["href"]) #print the options for the user to choose
    
    
    while True:
        selection = input("Please type the number of the film you want.") #loop so that the user chooses one the of the options of the search.
        try:
            if int(selection) in options.keys():
                break
        except:
            print("Try another option!")
    
    link = options[int(selection)]["href"].split("/?")[0]
    movie_id = link.split("title/")[1]

    return [link,movie_id] #return the link of the movie and the ID of the same. 

