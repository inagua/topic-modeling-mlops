import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler #, LabelEncoder  # , RobustScaler, robust_scale, MinMaxScaler
import argparse


def pca_dimension_reduction(embeddings):
    embeddings_data = np.load(embeddings)
    print("embeddings_data.shape: ", embeddings_data.shape)
    print("embeddings_data: ", embeddings_data)
    # le = LabelEncoder()
    # encoded = le.fit(embeddings)
    # np.set_printoptions(suppress=True)
    # embeddings = np.array(embeddings)
    # scaler = StandardScaler()
    # data_rescaled = scaler.fit_transform(embeddings_data)  # rescale embeddings
    # print("data_rescaled.shape: ", data_rescaled.shape)
    # print("data_rescaled: ", data_rescaled)
    # find the optimal number of components for PCA
    pca = PCA(n_components=0.95)
    result = pca.fit(embeddings_data)
    y = np.cumsum(result.explained_variance_ratio_)
    n_components = [index for index, value in enumerate(y) if value > 0.95][0]
    # apply PCA
    pca = PCA(n_components=n_components)
    output_pca_result = pca.fit_transform(embeddings_data)
    print("output_pca_result shape: ", output_pca_result.shape)
    print(" output_pca_result : ", output_pca_result)
    # write output_pca_result in a file
    np.save("pca_result.npy", output_pca_result)
    # return output_pca_result


if __name__ == '__main__':
    print("pca_dimension_reduction ... ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--embeddings')
    args = parser.parse_args()
    pca_dimension_reduction(args.embeddings)
    