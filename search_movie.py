from selenium import webdriver


def search_movies():
    #search= input('Search movies')
    search = "now you see me"
    website = 'https://www.imdb.com/'
    path = '/Users/mariavogli/Downloads/chromedriver'
    driver = webdriver.Chrome(path)
    driver.get(website)
    driver.find_element("id",'suggestion-search').send_keys(search)
    driver.find_element("id", 'suggestion-search-button').click()
    
    
    #driver.find_element("class_name",'result_text').text
    #driver.find_element("xpath",'//*[@id="main"]/div/div[2]/table/tbody/tr[1]/td[2]/a')
    #table=driver.find_elements("xpath",'//*[@id="main"]/div/div[2]/table')
    #rows=table.find_element("xpath",'//*[@id="main"]/div/div[2]/table/tbody/tr[1]/td[2]')
    #info = table.find_elements("tqg","td")
    res = driver.find_elements("class name","result_text")
    
    #rows=table.find_element("",'result_text')
    for row in res:
        name=row.getText()
        print(name)
    
    #return