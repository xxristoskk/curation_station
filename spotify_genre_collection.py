import spotipy
import json
import curation_station as cs
import functions as f
import pickle
from tqdm import tqdm
import pandas as pd

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


##### LOAD THE DATA ######

stuff = pickle.load(open('features_eda.pickle','rb'))
len(stuff)
pd.DataFrame(data=[pd.Series(x[1]) for x in stuff],index=[x[0] for x in stuff])

stuff[0][1].columns

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
    for i in range(1,len(list_of_df)):
        df = list_of_df[i][1].reset_index().rename(columns={'index':'genre'})
        df['genre'] = list_of_df[i][0]
        starter_df = pd.concat([starter_df,df])
    return starter_df

#### Drop the 'album' row and 'ep' ####
main_df = merge_dfs(stuff)

averages_df = main_df.groupby('genre').mean()
median_df = main_df.groupby('genre').median()
main_df.describe()

main_df.columns

main_df.drop(columns='analysis_url',inplace=True)

main_df

##### some quick plotting

corr = main_df.corr()

import plotly as py
import plotly.graph_objects as go

import plotly.express as px

# Here we use a column with categorical data
fig = px.histogram(main_df, x='genre')
fig.show()

import plotly.express as px
fig = px.scatter_matrix(main_df)
fig.show()


descriptive_df1 = main_df.groupby('genre').describe()

descriptive_df.min()

#### CLUSTERRS ?? #####
x = main_df.drop('genre',axis=1)
from sklearn.cluster import KMeans

km = KMeans(
    n_clusters=145, init='random',
    n_init=10, max_iter=300,
    tol=1e-04, random_state=0
)
y_km = km.fit_predict(x)

# plot the 3 clusters
plt.scatter(
    x[y_km == 0, 0], x[y_km == 0, 1],
    s=50, c='lightgreen',
    marker='s', edgecolor='black',
    label='cluster 1'
)

plt.scatter(
    x[y_km == 1, 0], x[y_km == 1, 1],
    s=50, c='orange',
    marker='o', edgecolor='black',
    label='cluster 2'
)

plt.scatter(
    x[y_km == 2, 0], x[y_km == 2, 1],
    s=50, c='lightblue',
    marker='v', edgecolor='black',
    label='cluster 3'
)

# plot the centroids
plt.scatter(
    km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
    s=250, marker='*',
    c='red', edgecolor='black',
    label='centroids'
)
plt.legend(scatterpoints=1)
plt.grid()
plt.show()


columns = list(genre_df['top_trax_feats'][0][0].keys())

list_of_feats = [x for n in genre_df['top_trax_feats'] for x in n]

pd.DataFrame(list_of_feats[0],index=list(genre_df.index))
