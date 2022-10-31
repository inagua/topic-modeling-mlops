import re
import argparse
import time
import pandas as pd
from pathlib import Path


def preprocess_input_text_(paragraph: str) -> pd.DataFrame:
    """Preprocesses a paragraph of text. Returns a dataframe with the following columns: paragraph (str)"""
    paragraph = paragraph.replace(r'\n', ' ', regex=True)
    # Remove new line characters
    paragraph = str(paragraph)
    paragraph = [re.sub('\s+', ' ', sent) for sent in paragraph]
    # remove unecessary newline characters
    paragraph = [re.sub('\\n', ' ', sent) for sent in paragraph]
    # Remove distracting single quotes
    paragraph = [re.sub("\'", "", sent) for sent in paragraph]
    paragraph = "".join(paragraph)
    # paragraph = str(paragraph)
    paragraph = paragraph.split(".")
    output_string = [sentence for sentence in paragraph if not int(len(sentence)) < 6]
    documents = {
        'paragraph': output_string
    }
    Path('paragraph.csv').touch()
    pd.DataFrame(documents).to_csv("paragraph.csv")


if __name__ == '__main__':
    print("Loading and preprocess_input_text_.....")
    time.sleep(1)
    print("Start.....")
    parser = argparse.ArgumentParser()
    parser.add_argument('--paragraph')
    args = parser.parse_args()
    preprocess_input_text_(args.paragraph)
