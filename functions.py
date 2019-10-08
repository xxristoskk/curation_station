## Last updated json Aug. 12, 2019
import spotipy
import json
import spotipy.util as util
import config
import time

scope = 'playlist-modify-public'

## Create auth token
token = util.prompt_for_user_token(config.username,
                                   scope,
                                   client_id=config.ClientID,
                                   client_secret=config.ClientSecret,
                                   redirect_uri='http://localhost/')
sp = spotipy.Spotify(auth=token)

## helper functions for pl_creator
def check_playlist(user, pl_name):
    for playlist in sp.user_playlists(user)['items']:
        if pl_name == playlist['name']:
            return playlist['id']
        else:
            return create_playlist(user,pl_name)['id']
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
    pl_id = check_playlist(user,pl_name)
    album_ids = []
    track_ids = []
    ## Search for albums in the dictionary
    for x in data:
        try:
            results = search_album(x['album'])
            album_name = results['albums']['items'][0]['name']
        except:
            data.remove(x) ## if the release can't be found on spotify, it is removed from from the search
        if album_name == x['album']:
            album_ids.append(results['albums']['items'][0]['id'])
        else:
            continue
    ## Put all found music into the playlist
    n = len(album_ids)
    i=0
    ## Adds 100 songs at a time
    while i < range(n):
        for z in range(99):
            track_ids.append(get_track_ids(album_ids[z]))
            i+=1
        add_to_playlist(user,pl_id,track_ids[:99])
        if i <= n:
            time.sleep(3)
            continue
        else:
            break
