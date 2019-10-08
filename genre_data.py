import curation_station as cs
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
from surprise import Dataset, Reader
from surprise import SVD
from surprise import accuracy
# from sklearn.metrics import classification_report, accuracy_score
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from surprise.model_selection import cross_validate, train_test_split


## Read json data from web scraping
# with open('/home/xristsos/Documents/nodata/bigNo.json') as json_data:
#     data = json.load(json_data)
# with open('/home/xristsos/Documents/nodata/big_G.json1') as json_data:
#     data2 = json.load(json_data)
# data_df = pd.DataFrame(data)


def organize_genres(d,num):
    no_list = ['EP','Album','Rock','Alternative','Indie','Country','Folk','EDM','Blues', 'Bluegrass']
    list1 = []
    list2 = []
    for i in range(len(d['genres'])):
        list1.append(d['genres'][i])
    for i in range(len(list1)):
        try:
            if list1[i][num] not in no_list:
                list2.append(list1[i][num])
            elif list1[i][num-1] not in no_list:
                list2.append(list1[i][num-1])
            elif list1[i][num+1] == True and list1[i][num+1] not in no_list:
                list2.append(list1[i][num+1])
            else:
                list2.append('N/A')
        except:
            list2.append('None')
    return list2

data_df['primary'] = organize_genres(data_df,0)
data_df['second'] = organize_genres(data_df,1)
data_df['third'] = organize_genres(data_df,2)
data_df['fourth'] = organize_genres(data_df,3)

genre_df = pd.DataFrame(data_df.drop(['genres','artist','date','album'],axis=1))
genre_df.shape
genre_df = pd.DataFrame(genre_df[genre_df['primary']!='N/A'])

# cs.get_genres(data)
# n = pd.DataFrame(cs.get_genres(data))
# data = cs.remove_duplicates(data)
# data_df.isna().sum()
data = cs.genre_dict_builder(data)
values = list(data.values())
df = pd.DataFrame([x.values() for x in values])
df.reset_index(inplace=True)
df.rename(columns={'index':'primary'},inplace=True)
df.fillna(0,inplace=True)


df.head()
reader = Reader(rating_scale=(0,200))
dta = Dataset.load_from_df(genre_df[['primary','second','third']],reader)


####################################################
# trainset, testset = train_test_split(data,test_size=.2)
dummy_df = pd.get_dummies(genre_df)
target = genre_df['primary']
labels = genre_df.drop('primary',axis=1)
from sklearn.model_selection import train_test_split
dummy_df.isna().sum()
dummies_df = pd.get_dummies(labels)
dummies_targe = pd.get_dummies(target)
xTrain,xTest,yTrain,yTest = train_test_split(dummies_df,dummies_targe, test_size=.2)
scaler = StandardScaler().fit(xTrain)
standard_x = scaler.transform(xTrain)
standard_xTest = scaler.transform(xTest)
scaled_df = pd.DataFrame(standard_x)
scaled_df.head()

from sklearn.cluster import KMeans
k_means = KMeans()
k_fit = k_means.fit(standard_x)
y_pred = k_fit.predict(standard_xTest)



from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(xTrain,yTrain)
test_preds = rf.predict(xTest)
test_scores(yTest,test_preds)
confusion_matrix(yTest,test_preds)
from sklearn.metrics import precision_score, recall_score,accuracy_score,f1_score, confusion_matrix,multilabel_confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier

gbc = GradientBoostingClassifier()
gbc.fit(xTrain,yTrain)

def test_scores(labels,preds):
    # print(f'Precision: {precision_score(labels,preds,average="micro")}')
    print(f'Recall: {recall_score(labels,preds,average="micro")}')
    print(f'Accuracy: {accuracy_score(labels,preds)}')
    print(f'F1 score: {f1_score(labels,preds,average="micro")}')

test_scores(yTest,test_preds)
find_best_k(xTrain,yTrain,xTest,yTest,min_k=1,max_k=25)
