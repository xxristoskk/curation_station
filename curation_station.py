## Last updated json Aug. 12, 2019
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import config
import functions as f


scope = 'playlist-modify-public'

## Create auth token
token = util.prompt_for_user_token(config.username,
                                   scope,
                                   client_id=config.ClientID,
                                   client_secret=config.ClientSecret,
                                   redirect_uri='http://localhost/')
sp = spotipy.Spotify(auth=token)

## Read json data from web scraping
with open('/home/xristsos/Documents/nodata/nodata1.json') as json_data:
    blog1 = json.load(json_data)
with open('/home/xristsos/Documents/nodata/glory_beats.json') as json_data:
    blog2 = json.load(json_data)


## Create functions that learns which two genres are often together
## Helper functions
def get_genres(data):
    lst = []
    rm_list = ['Album','Single','EP','Experimental','Various Artists','Dubstep']
    for x in data:
        for i in x['genres']:
            if i in rm_list:
                x['genres'].remove(i)
        lst.append(x['genres'])
    return lst

## Make a dictionary of genres
def genre_dict_builder(data):
    genre_list = get_genres(data)
    genre_dict = {}
    for genre in genre_list:
        for x in range(len(genre)):
            if genre[x-1] not in genre_dict:
                genre_dict[genre[x-1]] = {}
            if genre[x] not in genre_dict[genre[x-1]]:
                genre_dict[genre[x-1]][genre[x]] = 0
            genre_dict[genre[x-1]][genre[x]] += 1
    return genre_dict


## Finds the genre it gets paired with most and the least
# def genre_tuner(dictionary, genre):
#     if genre not in dictionary.keys():
#         print('Nothing found')
#     else:
#         tuple_values = list(dictionary[genre].items())
#     ## Find closest and furthest genre neighbor
#     i = 0
#     p = 2
#     first = ()
#     last = ()
#     for x in tuple_values:
#         if x[1] >= i:
#             i = x[1]
#             first = x
#         elif x[1] < p:
#             p = x[1]
#             last = x
#     return [first,last]

## Makes a new dataset based on focused genre
## Would like to have this take in a list of genres
# def curated_data(data, genres):
#     furthest_group = []
#     closest_group = []
#     for genre in genres:
#         neighbors = genre_tuner(genre_dict_builder(data),genre)
#         closest_group.append(neighbors[0][0])
#         furthest_group.append(neighbors[1][0])
#     new = []
#     for x in data:
#         for i in range(len(furthest_group)):
#             if furthest_group[i] in x['genres']:
#                 continue
#             elif closest_group[i] in x['genres']:
#                 new.append(x)
#     return new
#
# curated_data(big_data,['Techno','Bass'])


## Takes in a dictionary,username, and playlist name
## Returns a playlist with the first track from each album
def pl_creator(data, user, pl_name):
    pl_id = f.create_playlist(user,pl_name)['id']
    album_ids = []
    track_ids = []
    for x in data:
        try:
            results = f.search_album(x['album'])
            album_name = results['albums']['items'][0]['name']
        except:
            data.remove(x)
        if album_name == x['album']:
            album_ids.append(results['albums']['items'][0]['id'])
        else:
            continue
    for x in album_ids:
        track_ids.append(f.get_track_ids(x))
    f.add_to_playlist(user,pl_id,track_ids[0:99])
    return
