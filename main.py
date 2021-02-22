# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import re
from bs4 import BeautifulSoup

# 2000 top 2000/ 2010 / 2020 movies
url_00_movies = "https://www.imdb.com/search/title/?year=2000&title_type=feature&"  # top 2000 movies sorted by popularity
url_10_movies = "https://www.imdb.com/search/title/?year=2010&title_type=feature&"  # top 2010 movies sorted by popularity
url_20_movies = "https://www.imdb.com/search/title/?year=2020&title_type=feature&"  # top 2020 movies sorted by popularity
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
movieNames_10 = []
movieURL_10 = []
movieNames_20 = []
movieURL_20 = []


def getstats(url, div):
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
    getGenre = getContent.select(".genre , .scoreboard__info")
    genre = str(getGenre).split(",")[1]  # genre captured
    audienceScore = re.findall("audiencescore=\"(.*?)\"", str(selectContent))  # audience score captured
    tomatoScore = re.findall("tomatometerscore=\"(.*?)\"", str(selectContent))  # tomato score captured
    movieStats.append(genre)
    movieStats.append(tomatoScore)
    movieStats.append(audienceScore)
    return movieStats


def editmoviename(moviename):
    """
    Edits movie name to create url that navigates to tomatometer page for designated movie
    :param moviename
    :return: moviename
    """
    if " " in moviename:
        moviename = moviename.replace(" ", "_")
    if "?" in moviename:
        moviename = moviename.replace("?", "")
    if "-" in moviename:
        moviename = moviename.replace("-", "")
    if "," in moviename:
        moviename = moviename.replace(",", "")
    if "." in moviename:
        moviename = moviename.replace(".", "")
    if ":" in moviename:
        moviename = moviename.replace(":", "")
    # movie names with a non-uniform url hardcoded.
    if moviename == "shutter_island":
        moviename = "1198124-" + moviename
    if moviename == "kickass":
        moviename = "1217700-kick_ass"
    if moviename == "soul":
        moviename = moviename + "_2020"
    if moviename == "365_days":
        moviename = moviename + "_2020"
    return moviename



def getmovienamesimdb(div, movieNamesArr, movieURLArr,year):
    """
    retrieves top 10 popular movies of the following years: 2000, 2010, 2020
    :param moviename
    :return: moviename
    """
    moviecounter = 0
    for movies in div:
        if moviecounter < 10:
            movies = movies.text
            movieNamesArr.append(movies)

            movieNamesArr[moviecounter] = movieNamesArr[moviecounter].lower()

            movieNamesArr[moviecounter] = editmoviename(movieNamesArr[moviecounter])
            ## append movie name to end of tomatometer url + store in list
            tomatometerUrl = tomatometerUrlMain + movieNamesArr[moviecounter]
            movieURLArr.append(tomatometerUrl)
            moviestats = getstats(movieURLArr[moviecounter], ".scoreboard , .scoreboard__info")

            print("{} :: Movie: {} Genre: {} Tomatoscore: {} AudenienceScore: {}".format(year,movieNamesArr[moviecounter],
                                                                                   moviestats[0], moviestats[1],
                                                                                   moviestats[2]))

            tomatometerUrl = tomatometerUrlMain  # reset tomatometer Url
            moviecounter += 1

        else:
            break



test = getmovienamesimdb(top00movieNames_div, movieNames_00, movieURL_00, "'00")
test1 = getmovienamesimdb(top10movieNames_div, movieNames_10, movieURL_10, "'10")
test2 = getmovienamesimdb(top20movieNames_div, movieNames_20, movieURL_20, "'20")

