import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import argparse


def pca_dimension_reduction(embeddings: np.ndarray) -> np.ndarray:
    embeddings_data = np.load(embeddings)
    print("embeddings_data.shape: ", embeddings_data.shape)
    print("embeddings_data: ", embeddings_data)
    # scaler = StandardScaler()
    # data_rescaled = scaler.fit_transform(embeddings_data)  # rescale embeddings
    # find the optimal number of components for PCA
    pca = PCA(n_components=0.95)
    result = pca.fit(embeddings_data)
    y = np.cumsum(result.explained_variance_ratio_)
    n_components = [index for index, value in enumerate(y) if value > 0.95][0]
    # apply PCA
    pca = PCA(n_components=n_components)
    output_pca_result = pca.fit_transform(embeddings_data)
    # write output_pca_result in a file
    np.save("pca_result.npy", output_pca_result)


if __name__ == '__main__':
    print("pca_dimension_reduction ... ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--embeddings')
    args = parser.parse_args()
    pca_dimension_reduction(args.embeddings)
    