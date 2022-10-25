from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import argparse
import numpy as np
from pathlib import Path


def find_optimal_k_cluster(pca_result):
    pca_result_data = np.load(pca_result)
    print("pca_result.shape: ", pca_result_data.shape)
    print("pca_result: ", pca_result_data)
    # find the optimal number of clusters
    ks = range(2, 9)
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=ks)
    visualizer.fit(pca_result_data)
    output_n_clusters_optimal = visualizer.elbow_value_
    print("output_n_clusters_optimal: ", output_n_clusters_optimal)
    np.save("optimal_k_cluster.npy", output_n_clusters_optimal)
    # Path('optimal_k_cluster.txt').touch()
    # with open("optimal_k_cluster.txt", "w") as f:
    #     f.write((output_n_clusters_optimal))
    # return output_n_clusters_optimal


if __name__ == '__main__':
    print("find_optimal_k_cluster ... ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--pca_result')
    args = parser.parse_args()
    find_optimal_k_cluster(args.pca_result)
