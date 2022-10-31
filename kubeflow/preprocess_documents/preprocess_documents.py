import pandas as pd
import argparse
from pathlib import Path


def preprocess_documents_(documents_path):
    documents = pd.read_csv(documents_path)['documents']
    temp = []
    for i in range(len(documents)):
        documents[i] = documents[i].replace('[', '').replace(']', '').replace("'", '')
        documents[i] = documents[i].split(',')
        temp.append("".join(documents[i]))
    documents = temp
    output_documents = " ".join(documents)
    Path('documents.txt').touch()
    with open("documents.txt", 'w') as writer:
        writer.write(output_documents)


if __name__ == '__main__':
    print("Preprocessing documents ... ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--documents_path')
    args = parser.parse_args()
    preprocess_documents_(args.documents_path)
