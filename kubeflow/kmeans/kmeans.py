from sklearn.cluster import KMeans
import numpy as np
import argparse


def fit_kmeans_and_find_nearest_topic_clusters(n_clusters_optimal: int, pca_result: np.ndarray) -> np.ndarray:
    """ Fit KMeans to the PCA result and find the nearest topic clusters. Returns 5 nearest topic clusters for each cluster.
    -> top_nearest_indices_by_clusters.npy """
    pca_result = np.load(pca_result)
    n_clusters_optimal = int(np.load(n_clusters_optimal))
    kmeans_model = KMeans(n_clusters=int(n_clusters_optimal), random_state=0)
    kmeans_model.fit(pca_result)
    centers = np.array(kmeans_model.cluster_centers_)

    n = 5
    top_nearest_indices_by_clusters = []
    for cluster in range(len(centers)):
        ind = np.argsort(kmeans_model.transform(pca_result)[:, cluster])[:n]
        top_nearest_indices_by_clusters.append(ind)
    np.save('top_nearest_indices_by_clusters.npy', top_nearest_indices_by_clusters)


if __name__ == '__main__':
    print("find_optimal_k_cluster ... ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_clusters_optimal')
    parser.add_argument('--pca_result')
    args = parser.parse_args()
    fit_kmeans_and_find_nearest_topic_clusters(args.n_clusters_optimal, args.pca_result)
