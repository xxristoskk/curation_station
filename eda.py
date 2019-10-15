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
search_spotify(bc_artist_list[548635:])
sure = pickle.load(open('bc_confirmed.pickle','rb'))
len(sure)
##### checking for number of duplicates to handle #####
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

##### LOAD THE DATA ######

stuff = pickle.load(open('features_eda.pickle','rb'))

#### SET UP THE DATA, COLUMNS, AND INDEX FOR DF ######
list_of_genres = [x[0] for x in stuff]
for item in stuff:
    item[1].drop(columns=['track_href','id','type','uri'],inplace=True)
idk = {}
for item in stuff:
    idk[item[0]] = item[1]
idk.keys()

test = stuff[0][1].reset_index().rename(columns={'index':'genre'})
test['genre'] = 'techno'
test

#### function takes in the list of tuples and creates a new column 'genre' which is = [0] and the data comes from [1] #####
def merge_dfs(list_of_df):
    list_of_genres = [x[0] for x in list_of_df]
    starter_df = list_of_df[0][1].reset_index().rename(columns={'index':'genre'})
    starter_df['genre'] = list_of_genres[0]
    for i in tqdm(range(1,len(list_of_df))):
        df = list_of_df[i][1].reset_index().rename(columns={'index':'genre'})
        df['genre'] = list_of_df[i][0]
        starter_df = pd.concat([starter_df,df])
    return starter_df

#### Drop the 'album' row and 'ep' ####
main_df = merge_dfs(stuff)

averages_df = main_df.groupby('genre').mean()
median_df = main_df.groupby('genre').median()
main_df.describe()
main_df.drop(columns='analysis_url',inplace=True)
##### one-hot encoding #####
from sklearn.preprocessing import LabelEncoder

main_df

encoder = LabelEncoder()
labeld_genres = encoder.fit_transform(main_df['genre'])
main_df['encoded_genres'] = labeld_genres
encoded_df = main_df.drop(columns=['genre'])
##### some quick plotting

corr = main_df.corr()

import plotly as py
import plotly.graph_objects as go
import plotly.express as px

# Here we use a column with categorical data
fig = px.histogram(main_df, x='genre')
fig.show()
fig = px.scatter_matrix(encoded_df)
fig.show()

descriptive_df1 = main_df.groupby('genre').describe()
