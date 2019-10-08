import requests
import json
from bs4 import BeautifulSoup

""" bandcamp url formats =
https://{artistsname/url}.bancamp.com
https://bandcamp.com/tag/{genre}?tab=all_releases ### gives best selling
https://bandcamp.com/tag/{genre}?tab=all_releases&s=date ### gives new releases
https://bandcamp.com/tag/{genre}?tab=all_releases&s=date&t={second genre}%2C{third genre} ### adds second and third genre
https://bandcamp.com/tag/{city}
"""

### testing bandcamp scrape ###
url_best = 'https://bandcamp.com/tag/techno?tab=all_releases'
page_response = requests.get(url_best)
soup = BeautifulSoup(page_response.content,'html.parser')
body = soup.body
all_releases = list(body.find_all('div',class_='info'))
all_artists = [x.find('span').get_text() for x in all_releases]
all_titles = [x.find('div').get_text() for x in all_releases]

all_titles
all_artists

all_artists = clean_artists(all_artists)
all_titles = clean_titles(all_titles)

## Helper functions for scraper
def clean_titles(titles):
    for title in titles:
        if "\n" in title or title == "":
            titles.remove(title)
    return titles

def clean_artists(artists):
    for artist in artists:
        if len(artist) > 30 or "." in artist:
            artists.remove(artist)
        if artist == "":
            artists.remove(artist)
    return artists

### bandcamp scrape function ###
def scrape_bc(genres):
    stupid_list = []
    for genre in tqdm(genres):
        url_best = f'https://bandcamp.com/tag/{genre}?tab=all_releases'
        url_new = f'https://bandcamp.com/tage/{genre}?tab=all_releases&s=data'
        page_response = requests.get(url_best)
        soup = BeautifulSoup(page_response.content,'html.parser')
        body = soup.body
        all_releases = list(body.find_all('div',class_='info'))
        all_artists = [x.find('span').get_text() for x in all_releases]
        all_titles = [x.find('div').get_text() for x in all_releases]

        ## cleaner functions
        all_artists = clean_artists(all_artists)
        all_artists = clean_artists(all_artists)
        all_titles = clean_titles(all_titles)
        all_titles = clean_titles(all_titles)

        ## create release dictionary and append it
        for i in range(len(all_artists)):
            dictionary = {'artist': all_artists[i],
                          'album': all_titles[i],
                          'genres': genre}
            stupid_list.append(dictionary)
        time.sleep(1)
    return stupid_list

genre_list = list(genres.keys())

def clean_list(lst):
    clean = []
    for genre in lst:
        if " / " in genre:
            clean.append(genre.split(" / ")[1])
            clean.append(genre.split(" / ")[0])
        else:
            clean.append(genre)
    return clean

genre_list = clean_list(genre_list)

bc_data = scrape_bc(genre_list)

len(bc_data)
