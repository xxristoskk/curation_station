## Last updated json Aug. 12, 2019
import pandas as pd
import spotipy
import json

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

def genre_search(data, genres):
    new = []
    for x in data:
        if genres in x['genres']:
            new.append(x)
        else:
            continue
    return new
