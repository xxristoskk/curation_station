import spotipy
import json
import curation_station as cs
import functions as f
import pickle
from tqdm import tqdm


''' exploring ways to make a function that takes in a list of artist album_ids
    and returns audio features of their top tracks '''

# temp = pickle.load(open('bc_confirmed.pickle','rb'))
# temp[0][1]
# f.sp.artist('53giw2tzgMG8eDAmuaxdvR')
# top_tracks = get_top_tracks('53giw2tzgMG8eDAmuaxdvR')
# f.sp.audio_features(top_tracks)[0]
#
def get_top_tracks(artist_id):
    return [x['id'] for x in f.sp.artist_top_tracks(artist_id)['tracks']]
f.sp.audio_features(get_top_tracks('0N0d3kjwdY2h7UVuTdJGfp'))

# ''' another function that will take in a list of genres and return a dictionary
#     in the format {genre: [list of feature dictionaries]} or something like that '''
def spotify_genre_dict(genres):
    dictionary = {}
    for genre in tqdm(genres):
        artist_results = f.sp.search(q=f'genre:{genre}',type='artist')['artists']['items']
        artists = [(x['name'],x['id']) for x in artist_results]
        related_genres = [x['genres'] for x in artist_results]
        top_trax = [get_top_tracks(id) for artist,id in artists]
        top_trax = [item for sublist in top_trax for item in sublist]
        dictionary[genre] = {'related_genres': related_genres,
                             'artists': [item for sublist in top_trax for item in sublist],
                             'top_trax_feats': f.sp.audio_features(top_trax)}
        refresh_token()
    json.dump(dictionary,open('genre_definitions.json','w'))
    return dictionary

g = cs.genre_dict_builder(data)
g = list(g.keys())

genre_dict = spotify_genre_dict(g)

###### cleaning the genre list made from the keys of no/gb genre dict #####
def clean_list(lst):
    clean = []
    for genre in lst:
        if " / " in genre:
            clean.append(genre.split(" / ")[1])
            clean.append(genre.split(" / ")[0])
        else:
            clean.append(genre)
    return clean

g = clean_list(g)
for i in range(len(g)):
    g[i] = g[i].lower()
####### function to flatten out lists of lists (i made a lot of those and working against time) ######
### will fix this during refactoring phase ####
def flatten_lists(list_of_lists):
    return [x for y in list_of_lists for x in y]

''' the goal here is to create a dictionary of genres in that the values are the related genres and those genres have top features.
    trying to take the mean (or median) of the features of the subgenres. then taking the mean/median of all those and creating a
    standard defintion of the the root genre is composed of '''

genre_dict['techno'].keys()
genre_dict['techno']['related_genres']




###### DATAFRAME WORK CAUTION: UNDER HEAVY CONSTRUCTION ###############
''' cleaning the data frame and manipulating it to get the features as the columns and the rows being the genres but the features lists
    is a list of dataframes. i need go through each dataframe per genre, do heavy EDA, then take the averages of the features in order to have one singular
    value for each genre. after that i can start modeling.'''

genre_df = pd.DataFrame(genre_dict)
genre_df = genre_df.T.drop(columns='artists')
genre_df.reset_index(inplace=True)
genre_df.rename(columns={'index':'genre'},inplace=True)
for i,row in genre_df.iterrows():
    genre_df['related_genres'][i] = flatten_lists(genre_df['related_genres'][i])
for i,row in genre_df.iterrows():
    if len(genre_df['related_genres'][i]) < 1:
        genre_df.drop(i, inplace=True)
genre_df.head()

genre_df.set_index('genre',inplace=True)
genre_df['top_trax_feats'][0]

def features_dict_builder(list_of_dictionaries):
    new={}
    for col in columns:
        new[col] = []
    for d in list_of_dictionaries:
        for k,v in d.items():
            new[k].append(v)
    return new

f = features_dict_builder(genre_df['top_trax_feats'][0])

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

########## THIS IS A VERY IMPORT ZIP ############ it will be the basis for genre EDA before everything is put into one data frame
features_zipped = list(zip(list_of_genres,features))
# features_dict = {k:v for k,v in features_zipped}
# list(features_dict.keys())
features_dict['metal'].describe()

pickle.dump(features_zipped,open('features_eda.pickle','wb'))



###### TRYING TO MAKE DATAFRAME USING THE GENRE

columns = list(genre_df['top_trax_feats'][0][0].keys())

list_of_feats = [x for n in genre_df['top_trax_feats'] for x in n]

pd.DataFrame(list_of_feats[0],index=list(genre_df.index))
