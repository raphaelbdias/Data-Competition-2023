import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def build_model(dataframe):
    # Perform K-means clustering on the 'ori_latitude' feature
    K_clusters = range(1, 50)
    kmeans = [KMeans(n_clusters=i) for i in K_clusters]
    Y_axis = dataframe[['ori_latitude']]
    score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]
    
    # Visualize the Elbow Curve to determine the optimal number of clusters
    plt.plot(K_clusters, score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve')
    plt.show()

    # Perform K-means clustering on the 'ori_longitude' and 'ori_latitude' features
    X = dataframe[['ori_longitude', 'ori_latitude']]
    X1 = dataframe[['dest_longitude', 'dest_latitude']]

    # Cluster the 'ori_longitude' and 'ori_latitude' coordinates
    kmeans = KMeans(n_clusters=50, init='k-means++')
    kmeans.fit(X[X.columns[0:2]])
    X['cluster_label'] = kmeans.fit_predict(X[X.columns[0:2]])
    centers = kmeans.cluster_centers_
    labels = kmeans.predict(X[X.columns[1:3]])

    # Cluster the 'dest_longitude' and 'dest_latitude' coordinates
    kmeans1 = KMeans(n_clusters=50, init='k-means++')
    kmeans1.fit(X1[X1.columns[0:2]])
    X1['cluster_label'] = kmeans1.fit_predict(X1[X1.columns[0:2]])
    centers1 = kmeans1.cluster_centers_
    labels1 = kmeans1.predict(X1[X1.columns[1:3]])

    # Create a unique dataframe of clustered points
    X_un = X.drop_duplicates().dropna()
    X_un['clus_cat'] = X_un['cluster_label'].astype(str)
    
    return X_un