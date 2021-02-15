# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import re
from bs4 import BeautifulSoup

# Top DVD & Streaming
# url = "https://www.rottentomatoes.com/browse/top-dvd-streaming?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=popularity"
# url = "https://www.rottentomatoes.com/browse/tv-list-2"
# url = "https://www.rottentomatoes.com/browse/dvd-streaming-all"
url = "https://www.fandango.com/movie-reviews"

# 2000 top 2000/ 2010 / 2020 movies
url_00_movies = "https://www.imdb.com/search/title/?year=2000&title_type=feature&"  # top 2000 movies
url_10_movies = "https://www.imdb.com/search/title/?year=2010&title_type=feature&"  # top 2010 movies
url_20_movies = "https://www.imdb.com/search/title/?year=2020&title_type=feature&"  # top 2020 movies
response_00_movies = requests.get(url_00_movies)
response_10_movies = requests.get(url_10_movies)
response_20_movies = requests.get(url_20_movies)

top00moviesContent = BeautifulSoup(response_00_movies.text, 'html.parser')
top10moviesContent = BeautifulSoup(response_10_movies.text, 'html.parser')
top20moviesContent = BeautifulSoup(response_20_movies.text, 'html.parser')

top00movieNames_div = top00moviesContent.select(".lister-item-header a")
top10movieNames_div = top10moviesContent.select(".lister-item-header a")
top20movieNames_div = top20moviesContent.select(".lister-item-header a")

tomatometerUrlMain = "https://www.rottentomatoes.com/m/"
movieNames_00 = []
movieURL_00 = []
movieNames_10 = []  # TODO: 2010
movieURL_10 = []
movieNames_20 = []  # TODO: 2020
movieURL_20 = []


def getStats(url, div):
    """
    Scrapes movie page on tomatometer.com and grabs: genre, tomatometer score, and audience score.
    :param url:
    :param div:
    :return: List
    """
    movieStats = []
    getRequest = requests.get(url)
    getContent = BeautifulSoup(getRequest.text, 'html.parser')
    selectContent = getContent.select(div)
    genre = str(selectContent).split(",")[1]
    audienceScore = re.findall("audiencescore=\"(.*?)\"", str(selectContent))  # audience score captured
    tomatoScore = re.findall("tomatometerscore=\"(.*?)\"", str(selectContent))  # tomato score captured
    movieStats.append(genre)
    movieStats.append(tomatoScore)
    movieStats.append(audienceScore)
    return movieStats


## top 10 2000 movies.
x = 0
for movies in top00movieNames_div:
    if x < 10:
        movies = movies.text
        movieNames_00.append(movies)
        ## clean up string and transform into the format for tomatometer  url
        movieNames_00[x] = movieNames_00[x].lower()
        if " " in movieNames_00[x]:
            movieNames_00[x] = movieNames_00[x].replace(" ", "_")
        if "?" in movieNames_00[x]:
            movieNames_00[x] = movieNames_00[x].replace("?", "")
        if "-" in movieNames_00[x]:
            movieNames_00[x] = movieNames_00[x].replace("-", "")
        if "," in movieNames_00[x]:
            movieNames_00[x] = movieNames_00[x].replace(",", "")

        ## append movie name to end of tomatometer url + store in list
        tomatometerUrl = tomatometerUrlMain + movieNames_00[x]
        movieURL_00.append(tomatometerUrl)

        print(movieNames_00[x])
        print(movieURL_00[x])
        y = getStats(movieURL_00[x], ".scoreboard , .scoreboard__info")
        ##TODO: wrong genre
        ## Genre:  Where Art Thou?</h1>\n<p class="scoreboard__info" slot="info">200
        print("Movie: {} Genre: {} Tomatoscore: {} AudenienceScore: {}".format(movieNames_00[x], y[0], y[1], y[2]))

        tomatometerUrl = tomatometerUrlMain  # reset tomatometer Url
        x += 1

    else:
        break
