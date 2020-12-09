import requests
import json

def get_movies_from_tastedive(name=None):
    url = "https://tastedive.com/api/similar"
    dictionary = {}
    dictionary['type'] = 'movie'
    dictionary['q'] = name
    dictionary['limit'] = 5
    req = requests.get(url, params=dictionary)
    return json.loads(req.text)

def extract_movie_titles(dictionary={}):
    return [title["Name"] for title in dictionary["Similar"]["Results"]]

def get_related_titles(movies=[]):
    related_titles = []
    for movie in movies:
        query = get_movies_from_tastedive(movie)
        [related_titles.append(particular) for particular in extract_movie_titles(query)
            if particular not in related_titles]
    return related_titles

def get_movie_data(title=None):
    url = "http://www.omdbapi.com/?apikey=768159b3&"
    dictitonary = {}
    dictitonary['t'] = title
    dictitonary['r'] = "json"
    req = requests.get(url, params=dictitonary)
    print(type(json.loads(req.text)))
    return json.loads(req.text)

def get_movie_rating(dictionary={}):
    try:
        return int(dictionary['Ratings'][1]['Value'][:-1])
    except:
        return 0

def get_sorted_recommendations(movies=[]):
    recommendations = get_related_titles(movies)
    recommendations_titles = []
    for recommendation in recommendations:
        recommendations_titles.append(get_movie_data(recommendation))
    # print(json.dumps(recommendations_titles))
    return [title['Title'] for title in sorted(recommendations_titles, 
        key=lambda movie: (get_movie_rating(movie), movie['Title']),
        reverse=True)]


print(get_sorted_recommendations(("Venom, Baby Mama")))
