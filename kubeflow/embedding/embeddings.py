import numpy as np
import spacy
import argparse
import pandas as pd


def embedding(text):
    spacy.cli.download("en_core_web_sm")
    embed = spacy.load("en_core_web_sm")
    text = np.array(pd.read_csv(text)['paragraph'])
    data_list = [embed(doc).vector.reshape(1, -1) for doc in text]
    # np.set_printoptions(suppress=True)
    output_embeddings = np.concatenate(data_list)
    # write output_embeddings in a file
    # output_embeddings_path = "./app/embeddings.npy"
    # np.save(output_embeddings_path, output_embeddings)
    np.save('embedding.npy', output_embeddings)
    # with open(output_embeddings_path, 'w') as f:
    #     f.write(str(output_embeddings))


if __name__ == '__main__':
    print("Embedding ...")
    parser = argparse.ArgumentParser()
    parser.add_argument('--paragraph')
    args = parser.parse_args()
    embedding(args.paragraph)
    print("Embedding done.")
