# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup

#Top DVD & Streaming
url = "https://www.rottentomatoes.com/browse/top-dvd-streaming?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=popularity"
response = requests.get(url)

main_page_content = BeautifulSoup(response.text, 'html.parser')
# print(main_page_content)


topMovieHits = main_page_content.select(".titleColumn")
print(topMovieHits) ## printing empty array


