import pandas as pd
import numpy as np
import argparse


def create_dataframe_from_top_nearest_indices(top_nearest_indices_by_clusters: np.ndarray, text: str) -> pd.DataFrame:
    text = pd.read_csv(text)['paragraph']
    top_nearest_indices_by_clusters = np.load(top_nearest_indices_by_clusters)
    all_documents = []
    for cluster in top_nearest_indices_by_clusters:
        document = []
        for index in cluster:
            if int(len(text[index]) <= int(4)): continue
            text[index] = text[index] + ". "
            document.append(text[index])
        all_documents.append(document)
    courses = {
        'documents': all_documents
    }
    documents = pd.DataFrame(courses)
    documents.to_csv("documents.csv")


if __name__ == '__main__':
    print("create_dataframe_from_top_nearest_indices ... ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--top_nearest_indices_by_clusters')
    parser.add_argument('--text')
    args = parser.parse_args()
    create_dataframe_from_top_nearest_indices(args.top_nearest_indices_by_clusters, args.text)

    