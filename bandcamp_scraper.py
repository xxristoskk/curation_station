import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle
import time

### artist index scrape ###
''' this function takes a number representing the number of pages needed to be scraped
    and iterates the scraping process for each page. the returned data is a list of all the
    artist names that are in the bandcamp artist index and will be used as a reference when
    looking for new artists to match search parameters '''
def get_all_artists(pages):
    artist_list = []
    for i in tqdm(range(1, pages)):
        try:
            open('bc_artists.pickle','a')
            url = f'https://bandcamp.com/artist_index?page={i}'
            r = requests.get(url)
            soup = BeautifulSoup(r.text,'html.parser')
            body = soup.body
            item_list = soup.find('ul',class_='item_list')
            items = list(item_list.find_all('li',class_='item'))
            artist_list.extend([x.find('div',class_='itemtext').get_text() for x in items])
            pickle.dump(artist_list,open('bc_artists.pickle','wb'))
            time.sleep(2)
        except:
            print("it done")
            pickle.dump(artist_list,open('bc_artists.pickle','wb'))
            break
    return

get_all_artists(2973)

n = pickle.load(open('bc_artists.pickle','rb'))
len(n)

# bandcamp url formats =
# https://{artistsname/url}.bancamp.com
# https://bandcamp.com/tag/{genre}?tab=all_releases ### gives best selling
# https://bandcamp.com/tag/{genre}?tab=all_releases&s=date ### gives new releases
# https://bandcamp.com/tag/{genre}?tab=all_releases&s=date&t={second genre}%2C{third genre} ### adds second and third genre
# https://bandcamp.com/tag/{city}


### testing bandcamp scrape ###
# url_best = 'https://bandcamp.com/tag/techno?tab=all_releases'
# page_response = requests.get(url_best)
# soup = BeautifulSoup(page_response.content,'html.parser')
# body = soup.body
# all_releases = list(body.find_all('div',class_='info'))
# all_artists = [x.find('span').get_text() for x in all_releases]
# all_titles = [x.find('div').get_text() for x in all_releases]
#
# all_titles
# all_artists
#
# all_artists = clean_artists(all_artists)
# all_titles = clean_titles(all_titles)


# ## Helper functions for scraper
# def clean_titles(titles):
#     for title in titles:
#         if "\n" in title or title == "":
#             titles.remove(title)
#     return titles
#
# def clean_artists(artists):
#     for artist in artists:
#         if len(artist) > 30 or "." in artist:
#             artists.remove(artist)
#         if artist == "":
#             artists.remove(artist)
#     return artists
#
#
# ### bandcamp scrape function ###
# ######## used to find trending diy artists on bandcamp
# def scrape_bc(genres):
#     bc_list = []
#     for genre in tqdm(genres):
#         url_best = f'https://bandcamp.com/tag/{genre}?tab=all_releases'
#         url_new = f'https://bandcamp.com/tage/{genre}?tab=all_releases&s=data'
#         page_response = requests.get(url_best)
#         soup = BeautifulSoup(page_response.content,'html.parser')
#         body = soup.body
#         all_releases = list(body.find_all('div',class_='info'))
#         all_artists = [x.find('span').get_text() for x in all_releases]
#         all_titles = [x.find('div').get_text() for x in all_releases]
#
#         ## cleaner functions
          ##### for whatever reason, the cleaner functions don't clean the first time around but work when the list is ran through twice
#         all_artists = clean_artists(all_artists)
#         all_artists = clean_artists(all_artists)
#         all_titles = clean_titles(all_titles)
#         all_titles = clean_titles(all_titles)
#
#         ## create release dictionary and append it
#         for i in range(len(all_artists)):
#             dictionary = {'artist': all_artists[i],
#                           'album': all_titles[i],
#                           'genre': genre}
#             bc_list.append(dictionary)
#         time.sleep(1)
#     return bc_list
#
#
# def clean_list(lst):
#     clean = []
#     for genre in lst:
#         if " / " in genre:
#             clean.append(genre.split(" / ")[1])
#             clean.append(genre.split(" / ")[0])
#         else:
#             clean.append(genre)
#     return clean
#
#
# genre_list = clean_list(genre_list)
#
# bc_data = scrape_bc(genre_list)
