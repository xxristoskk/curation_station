import pandas as pd
import json

nd = json.load(open('bigNoOct7.json','r'))
gb = json.load(open('glory_oct7.json','r'))
data = nd + gb
#### EXPLORING THE DATAFRAME ####
df = pd.DataFrame(data)

df.shape
df.head()
df.isna().sum()

df.sort_values(by='date')

### NLP on genres?? ### genre matrix ###
genre_matrix = pd.DataFrame(genres)
