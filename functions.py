## Last updated json Aug. 12, 2019
import spotipy
import json
import spotipy.util as util
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import config
import time


## Create auth token
scope = 'playlist-modify-public'
# token = util.prompt_for_user_token(config.username,
#                                    scope,
#                                    client_id=config.ClientID,
#                                    client_secret=config.ClientSecret,
#                                    redirect_uri='http://localhost/')
# sp = spotipy.Spotify(auth=token)

##################### oauth2 for token refreshing (work in progress) ###########################
####### is_token_expired attribute isn't working for spotipy so declaring it from the latest version oauth2.py on the github
def is_token_expired(token_info):
    now = int(time.time())
    return token_info['expires_at'] - now < 60

oauth = SpotifyOAuth(client_id=config.ClientID,client_secret=config.ClientSecret,redirect_uri='http://localhost/',scope=scope)
token_info = oauth.get_cached_token()
if not token_info:
    auth_url = oauth.get_authorize_url()
    print(auth_url)
    response = input('Paste the above link into your browser, then paste the redirect url here: ')
    code = oauth.parse_response_code(response)
    token_info = oauth.get_access_token(code)
    token = token_info['access_token']
sp = spotipy.Spotify(auth=token)

def refresh_token():
    global token_info, sp
    if is_token_expired(token_info):
        token_info = oauth.refresh_access_token(token_info['refresh_token'])
        token = token_info['access_token']
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
def find_artist(artist_name):
    return sp.search(q='artist:' + artist_name, type='artist')

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
