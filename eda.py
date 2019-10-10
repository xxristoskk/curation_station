import spotipy
import pandas as pd
import json
import curation_station as cs
import functions as f
import pickle

nd = json.load(open('/home/xristsos/Documents/nodata/bigNoOct7.json','r'))
gb = json.load(open('/home/xristsos/Documents/nodata/glory_oct7.json','r'))

data = nd + gb
data = cs.remove_duplicates(data)


############### Spotify things ##########################
bc_artist_list = pickle.load(open('bc_artists.pickle','rb'))
len(bc_artist_list)
bc_artist_list[-1]
f.search_album('Warmwoods')
sp.album_tracks('5TcTn4bGDBYGRtISkpW4Rg')
sp.audio_analysis('5rkfm2WfRFre6LZ5BWAQ5f') ##### very detailed analysis of the audio from the start to finish -- needs in depth exploring and comparing with others
################################################# in the genre. find patterns in song structure, call and response, drops, builds, ect.

## grab artist ID in items[0]['id']
find_artist('The Darien Venture') ### if total less than 1 then the artist isn't on spotify
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
