import os

def run():
    #Given that the imdb_main module needs to be called on the terminal by python and that the streamlit module needs to be called with the streamlit module,
    #this short scripts calles the two main modules of the project. 
    #the imdb_main module handles the creation of a movie, filling its information and calling the methods to scrap the recommended films.
    #the stream_show module handles the movie saved in mongoDB and generates the dashboard with the plots to study. 
    os.system("python imdb_main.py")
    os.system("streamlit run stream_show.py")
run()