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
nd = json.load(open('/home/xristsos/Documents/nodata/bigNoOct7.json','r'))
gb = json.load(open('/home/xristsos/Documents/nodata/glory_oct7.json','r'))
unsure = pickle.load(open('bc_unsure.pickle','rb'))

data = nd + gb
data = cs.remove_duplicates(data)
bc_artist_list = pickle.load(open('bc_artists.pickle','rb'))

def search_spotify(bc_list):
    """ takes in the list of bandcamp artists and searches for them on spotify
    if they are on spotify the artist is added to a new list """
    new_list = pickle.load(open('bc_confirmed.pickle','rb')) ### all the artists confirmed to be on spotify
    # fuzzy_list = pickle.load(open('bc_unsure.pickle','rb')) ### list of search results that totaled more than 1 artist
    for artist in tqdm(bc_list):
        f.refresh_token()
        results = f.find_artist(artist)
        if results['artists']['total'] < 1:
            continue
        elif results['artists']['total'] == 1:
            new_list.append((artist,results['artists']['items'][0]['id']))
            pickle.dump(new_list,open('bc_confirmed.pickle','wb'))
        # elif results['artists']['total'] > 1:
        #     fuzzy_list.append(results)
        #     pickle.dump(fuzzy_list,open('bc_unsure.pickle','wb'))
    return
19760+329500
search_spotify(bc_artist_list[349260:])
sure = pickle.load(open('bc_confirmed.pickle','rb'))
# unsure = pickle.load(open('bc_unsure.pickle','rb'))
len(sure)
# len(unsure)
# len(sure) + len(unsure)
hit_list = []
counter = 0
for x in tqdm(sure):
    if x in hit_list and x in sure:
        counter+=1
    elif x not in hit_list:
        hit_list.append(x)
counter

############### Spotify search from bandcamp database ##########################
bc_artist_list = pickle.load(open('bc_artists.pickle','rb'))
len(bc_artist_list)
bc_artist_list[-1]
f.search_album('Warmwoods')
sp.album_tracks('5TcTn4bGDBYGRtISkpW4Rg')
sp.audio_analysis('5rkfm2WfRFre6LZ5BWAQ5f') ##### very detailed analysis of the audio from the start to finish -- needs in depth exploring and comparing with others
################################################# in the genre. find patterns in song structure, call and response, drops, builds, ect.

## grab artist ID in items[0]['id']
f.find_artist('The Darien Venture')['artists']['items'][0]['id'] ### if total less than 1 then the artist isn't on spotify
sp.artist_albums('1XaiQhSCl8fM7PfEwr06st') ## gets the albums from the artist -- needs to be explored to find the first one
f.get_track_ids('5eletkEtPTsiMKmlcS3TMe') ## returns id of first track from album -- lets grab 2 tracks in the future
sp.audio_features('55qSasiM8jQSyNo0Hi3gNE') #### This brings back valence dancability and all that stuff -- will use later
######################### Pandas things ###################3


pd.DataFrame(data)

#### EXPLORING THE DATAFRAME ####
df = pd.DataFrame(data)

df.shape
df.head()
df.isna().sum()

df.sort_values(by='date')

### NLP on genres?? ### genre matrix ###
genre_matrix = pd.DataFrame(genres)
