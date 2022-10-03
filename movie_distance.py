from scipy.spatial import distance


def compare_lists(list1,list2):
    #This functions takes two lists and estimates how similar the second list is to the first one. Result might be between 0 and 1.
    list1 = list(set(list1))
    list2 = list(set(list2))
    common_elements = len(set(list1) & set(list2))    
    common_elements_proportion = common_elements / len(list1)
    return common_elements_proportion


def estimateMovieDistance(movie1,movie2):
    movie1_vector = [movie1["year_released"],movie1["runtime"],movie1["imdb_reviews"],movie1["external_reviews"],movie1["imdb_rating"],movie1["metacritic_punctuation"],movie1["budget"],
                    movie1["earning_worldwide"],movie1["earning_US&CA"],1,1,1]
    movie2_vector = [movie2["year_released"],movie2["runtime"],movie2["imdb_reviews"],movie2["external_reviews"],movie2["imdb_rating"],movie2["metacritic_punctuation"],movie2["budget"],
                    movie2["earning_worldwide"],movie2["earning_US&CA"]]
    
    common_genres_rate = compare_lists(movie1["genres"],movie2["genres"])
    movie2_vector.append(common_genres_rate)

    common_directors_rate = compare_lists(movie1["directors"],movie2["directors"])
    movie2_vector.append(common_directors_rate)

    common_cast_rate = compare_lists(movie1["cast"],movie2["cast"])
    movie2_vector.append(common_cast_rate)

    euclidean = distance.euclidean(movie1_vector,movie2_vector)
    manhattan = distance.cityblock(movie1_vector,movie2_vector)
    manhattan = manhattan.item()
    
    return euclidean,manhattan

