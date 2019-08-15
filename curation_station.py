## Last updated json Aug. 12, 2019
import spotipy
import json
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
with open('glory_beats.json') as json_data:
    glory_data = json.load(json_data)
with open('nodata1.json') as json_data2:
    nd_data = json.load(json_data2)

data = glory_data + nd_data
## Create functions that learns which two genres are often together
## Helper functions
def get_genres(data):
    lst = []
    ## List all the tags/gnres you don't want in your playlist
    ## Removing general genres or tags like Electronic or Album will yield more curated results
    rm_list = ['Album','Single','EP','Experimental','Various Artists','Dubstep','Electronic']
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

# Finds the genre it gets paired with most
def genre_tuner(dictionary, genre):
    genre_tuples = []
    first = ''
    if genre not in dictionary.keys():
        print('Nothing found')
    else:
        genre_tuples = list(dictionary[genre].items())
    i = 0
    for x in genre_tuples:
        if x[1] >= i:
            i = x[1]
            first = x[0]
    return first

# Makes a new dataset based on focused genre
# Would like to have this take in a list of genres
def curated_data(data, genre):
    genre = genre.title()
    neighbor = genre_tuner(genre_dict_builder(data),genre)
    new = []
    for x in data:
        if neighbor not in x['genres']:
            continue
        else:
            new.append(x)
    return new


## helper functions for pl_creator
def create_playlist(user,name):
    return sp.user_playlist_create(user,name)
def search_album(album):
    return sp.search(q='album:' + album, type='album')
def add_to_playlist(user, playlist_id, track_id):
    return sp.user_playlist_add_tracks(user, playlist_id, track_id)
def get_track_ids(album_id):
    return sp.album_tracks(album_id)['items'][0]['id']

## Takes in a dictionary,username, and playlist name
## Returns a playlist with the first track from each album
def pl_creator(data, user, pl_name):
    pl_id = create_playlist(user,pl_name)['id']
    album_ids = []
    track_ids = []
    for x in data:
        try:
            results = search_album(x['album'])
            album_name = results['albums']['items'][0]['name']
        except:
            data.remove(x)
        if album_name == x['album']:
            album_ids.append(results['albums']['items'][0]['id'])
        else:
            continue
    for x in album_ids:
        track_ids.append(get_track_ids(x))
    add_to_playlist(user,pl_id,track_ids[0:99])
    return

pl_creator(curated_data(data,'Industrial'), config.username, 'hard dance')

# def test(data):
#     album_ids = []
#     for x in data:
#         results = search_album(x['album'])
#         album_name = results['albums']['items'][0]['name']
#         if album_name == x['album']:
#             album_ids.append(results['albums']['items'][0]['id'])
#     return album_ids
