import spotipy as sp
import json
import curation_station as cs
import functions as f
import pickle
from tqdm import tqdm
import pandas as pd

''' exploring ways to make a function that takes in a list of artist album_ids
    and returns audio features of their top tracks '''

def get_top_tracks(artist_id):
    return [x['id'] for x in f.sp.artist_top_tracks(artist_id)['tracks']]

''' another function that will take in a list of genres and return a dictionary
    in the format {genre: [list of feature dictionaries]} or something like that '''
def spotify_genre_dict(genres):
    dictionary = {}
    for genre in tqdm(genres):
        artist_results = sp.search(q=f'genre:{genre}',type='artist')['artists']['items']
        artists = [(x['name'],x['id']) for x in artist_results]
        related_genres = [x['genres'] for x in artist_results]
        top_trax = [get_top_tracks(id) for artist,id in artists]
        top_trax = [item for sublist in top_trax for item in sublist]
        dictionary[genre] = {'related_genres': related_genres,
                             'artists': [item for sublist in top_trax for item in sublist],
                             'top_trax_feats': f.sp.audio_features(top_trax)}
        f.refresh_token()
    json.dump(dictionary,open('genre_definitions.json','w'))
    return dictionary

###### cleaning the genre list made from the keys of no/gb genre dict #####
def clean_list(lst):
    clean = []
    for genre in lst:
        genre = genre.lower()
        if " / " in genre:
            clean.append(genre.split(" / ")[1])
            clean.append(genre.split(" / ")[0])
        else:
            clean.append(genre)
    return clean

g = cs.genre_dict_builder(data)
g = list(g.keys())
g = clean_list(g)
genre_dict = spotify_genre_dict(g)
pickle.dump(genre_dict,open('genre_dictionary.pickle','wb'))


####### function to flatten out lists of lists (i made a lot of those and working against time) ######
### will fix this during refactoring phase ####

def flatten_lists(list_of_lists):
    return [x for y in list_of_lists for x in y]

''' the goal here is to create a dictionary of genres in that the values are the related genres and those genres have top features.
    trying to take the mean (or median) of the features of the subgenres. then taking the mean/median of all those and creating a
    standard defintion of the the root genre is composed of '''

genre_dict = pickle.load(open('genre_dictionary.pickle','rb'))

### flatten related genres lists ###
for k,v in genre_dict.items():
    v['related_genres'] = flatten_lists(['related_genres'])

#### remove top track features
def genre_matrix(d):
    new_dict = {}
    ### extracting just the root genre and the related genres
    for k,v in d.items():
        for i,n in v.items():
            if i == 'related_genres':
                new_dict[k] = n
    for k,v in new_dict.items():
        if len(v) >= 5:
            v = flatten_lists(v)
            v = flatten_lists(v)
        else:
            continue
    return new_dict

genre_matrix = genre_matrix(genre_dict)
genre_matrix

###### DATAFRAME WORK CAUTION: UNDER HEAVY CONSTRUCTION ###############
''' cleaning the data frame and manipulating it to get the features as the columns and the rows being the genres but the features lists
    is a list of dataframes. i need go through each dataframe per genre, do heavy EDA, then take the averages of the features in order to have one singular
    value for each genre. after that i can start modeling.'''

genre_df = pd.DataFrame(genre_dict)
genre_df = genre_df.T.drop(columns='artists')
genre_df.reset_index(inplace=True)
genre_df.rename(columns={'index':'genre'},inplace=True)
# for i,row in genre_df.iterrows():
#     genre_df['related_genres'][i] = flatten_lists(genre_df['related_genres'][i])
# for i,row in genre_df.iterrows():
#     if len(genre_df['related_genres'][i]) < 1:
#         genre_df.drop(i, inplace=True)
genre_df.head()
related_df = genre_df.drop(columns='top_trax_feats')

related_df.set_index('genre',inplace=True)
for i,row in related_df.iterrows():
    related_df['related_genres'][i] = flatten_lists(related_df['related_genres'][i])
related_df

def features_dict_builder(list_of_dictionaries):
    new={}
    for col in columns:
        new[col] = []
    for d in list_of_dictionaries:
        for k,v in d.items():
            new[k].append(v)
    return new

def series2df(df):
    dfs = []
    for i in range(len(df)):
        try:
            dfs.append(pd.DataFrame(features_dict_builder(df['top_trax_feats'][i])))
        except:
            print(i)
            continue
    return dfs

genre_df.reset_index(inplace=True)

genre_df.drop([17,46,55,93],inplace=True)
features = series2df(genre_df)
features[0]


cols_to_drop = ['type','uri','track_href']

features_df = pd.concat(features)

len(features)
genre_df.shape
genre_df.set_index('genre',inplace=True)
list_of_genres = list(genre_df.index)

########## approach below is best ############
features_zipped = list(zip(list_of_genres,features))
# features_dict = {k:v for k,v in features_zipped}
# list(features_dict.keys())
features_dict['metal'].describe()

pickle.dump(features_zipped,open('features_eda.pickle','wb'))
