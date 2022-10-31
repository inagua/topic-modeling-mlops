from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import argparse
import numpy as np


def find_optimal_k_cluster(pca_result: np.ndarray) -> int:
    pca_result_data = np.load(pca_result)
    # find the optimal number of clusters
    ks = range(2, 9)
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=ks)
    visualizer.fit(pca_result_data)
    output_n_clusters_optimal = visualizer.elbow_value_
    np.save("optimal_k_cluster.npy", output_n_clusters_optimal)


if __name__ == '__main__':
    print("find_optimal_k_cluster ... ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--pca_result')
    args = parser.parse_args()
    find_optimal_k_cluster(args.pca_result)
