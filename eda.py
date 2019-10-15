import spotipy
import pandas as pd
import json
import curation_station as cs
import functions as f
import pickle
from tqdm import tqdm
import time
from threading import Timer

##### Load the saved data
nd = json.load(open('/home/xristos/Documents/bigNoOct7.json','r'))
gb = json.load(open('/home/xristos/Documents/glory_oct7.json','r'))

data = nd + gb
data = cs.remove_duplicates(data)
bc_artist_list = pickle.load(open('bc_artists.pickle','rb'))

def search_spotify(bc_list):
    """ takes in the list of bandcamp artists and searches for them on spotify
    if they are on spotify the artist is added to a new list """
    t = Timer(3000.0, f.refresh_token())
    new_list = pickle.load(open('bc_confirmed.pickle','rb'))
    fuzzy_list = pickle.load(open('bc_unsure.pickle','rb'))
    # new_list = []
    # fuzzy_list = [] ##### for search results that return more than one possible artist -- needs further exploring
    t.start()
    for artist in tqdm(bc_list):
        results = f.find_artist(artist)
        if results['artists']['total'] < 1:
            continue
        elif results['artists']['total'] == 1:
            new_list.append((artist,results['artists']['items'][0]['id']))
            pickle.dump(new_list,open('bc_confirmed.pickle','wb'))
        elif results['artists']['total'] > 1:
            fuzzy_list.append(results)
            pickle.dump(fuzzy_list,open('bc_unsure.pickle','wb'))
        f.refresh_token()
    return new_list, fuzzy_list

sure,unsure = search_spotify(bc_artist_list[57958:])

sure = pickle.load(open('bc_confirmed.pickle','rb'))
unsure = pickle.load(open('bc_unsure.pickle','rb'))
len(sure)
len(unsure)
len(sure) + len(unsure)
sure[:100]
############### Spotify search from bandcamp database ##########################
bc_artist_list = pickle.load(open('bc_artists.pickle','rb'))
len(bc_artist_list)
bc_artist_list[-1]
f.search_album('Warmwoods')
sp.album_tracks('5TcTn4bGDBYGRtISkpW4Rg')
sp.audio_analysis('5rkfm2WfRFre6LZ5BWAQ5f') ##### very detailed analysis of the audio from the start to finish -- needs in depth exploring and comparing with others
################################################# in the genre. find patterns in song structure, call and response, drops, builds, ect.


######################### Pandas things ###################3
#### EXPLORING THE DATAFRAME ####
df = pd.DataFrame(data)

df.shape
df.head()
df.isna().sum()

df.sort_values(by='date')

### exploring the genre dataframe ###
genre_df = json.load(open('genre_definitions.json','r'))
