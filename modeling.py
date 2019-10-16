from sklearn.cluster import KMeans
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.metrics import accuracy_score, auc, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.metrics.cluster import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KDTree, KNeighborsClassifier,NearestNeighbors,NeighborhoodComponentsAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

kmeans = KMeans(n_clusters=145).fit(encoded_df)

centroids = kmeans.cluster_centers_
print(centroids)
encoded_df.columns
import matplotlib.pyplot as plt
plt.scatter(encoded_df['encoded_genres'],encoded_df['instrumentalness'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)


encoded_df.columns
y = encoded_df['encoded_genres']
X = encoded_df.drop(columns='encoded_genres')

xTest,xTrain,yTest,yTrain = train_test_split(X,y,test_size=.2,random_state=20)

knn = KNeighborsClassifier()
knn.fit(xTrain,yTrain)
