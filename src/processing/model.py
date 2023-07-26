from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import processing.parser as pr

def train_clustering_model(data, clusters):
    model = KMeans(n_clusters = clusters, random_state = 15, n_init='auto')
    model.fit(data.to_numpy())
    return model

def count_wcss(data):
    wcss = [] 
    for number_of_clusters in range(1, 11): 
        model = KMeans(n_clusters = number_of_clusters, random_state = 42)
        model.fit(data.to_numpy()) 
        wcss.append(model.inertia_)
    return wcss

def get_knn(user, data, n_neigh):
    neigh = NearestNeighbors(n_neighbors=n_neigh)
    neigh.fit(data)
    return neigh.kneighbors([user])

def get_knn_for_types(user, data, n_neigh):
    res_ids = []
    types = data[['type']].drop_duplicates().values
    for type_t in types:
        neigh = NearestNeighbors(n_neighbors=n_neigh)
        slice = data[data['type'] == type_t[0]]
        neigh.fit(slice[pr.columns_normilized].values)
        _, ids = neigh.kneighbors([user])
        res_ids += slice.iloc[ids[0]]['osmid'].values.tolist()
    print(res_ids)
    return pd.concat([data[data['osmid'] == id] for id in res_ids])
        