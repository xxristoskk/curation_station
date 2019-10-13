import spotipy
import json
import curation_station as cs
import functions as f
import pickle
from tqdm import tqdm


''' exploring ways to make a function that takes in a list of artist album_ids
    and returns audio features of their top tracks '''
temp = pickle.load(open('bc_confirmed.pickle','rb'))
temp[0][1]
f.sp.artist('53giw2tzgMG8eDAmuaxdvR')
top_tracks = [x['id'] for x in get_top_tracks('53giw2tzgMG8eDAmuaxdvR')['tracks']]
f.sp.audio_features(top_tracks)[0]

def get_top_tracks(artist_id):
    return f.sp.artist_top_tracks(artist_id=artist_id)

f.sp.recommendation_genre_seeds()
f.sp.search(q='genre:techno',type='artist')
