from sklearn.cluster import KMeans

def train_model(data, clusters):
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