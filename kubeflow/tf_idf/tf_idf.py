from pathlib import Path

from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import gensim
from gensim.utils import simple_preprocess
import spacy
import pandas as pd
import argparse
import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords = stopwords.words("english")
stopwords.extend(['from', 'subject', 're', 'edu', 'use'])


def gen_words(texts):
    for i in range(len(texts)):
        texts[i] = texts[i].replace('[', '').replace(']', '').replace("'", '')
        texts[i] = "".join(texts[i])
        print("texts[i] : ", texts[i])
        texts[i] = texts[i].split(".")
        # if texts[i] <= 6: continue
    print("texts : ", texts)
    final = []
    for text in texts:
        new = yield simple_preprocess(str(text), deacc=True)  # deacc True remove punctuations
        final.append(new)
    return final


def create_bigram_trigram(data_words):
    # Creating Bigram and Trigram models
    '''
        Bigrams are 2 words frequently occuring together in docuent.
        Trigrams are 3 words frequently occuring.
        Many other techniques are explained in part-1 of the blog which are important in NLP pipline, it would be worth your while going through that blog.
        The 2 arguments for Phrases are min_count and threshold. The higher the values of these parameters , the harder its for a word to be combined to bigram.

    '''

    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    # higher threshold fewer phrases
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    # faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    return bigram_mod, trigram_mod


def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stopwords] for doc in texts]


def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]


def make_trigrams(texts, trigram_mod, bigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append(" ".join([token.lemma_ for token in doc if token.pos_ in allowed_postags]))
    return texts_out


def tf_idf(documents: Path) -> pd.DataFrame:

    documents = pd.read_csv(documents)['documents']
    data_words = list(gen_words(documents))
    bigram_mod, trigram_mod = create_bigram_trigram(data_words)
    # remove stopwords
    data_words_nostops = remove_stopwords(data_words)
    # form bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    data_lemmatized = lemmatization(data_words_bigrams)

    tfIdfVectorizer = TfidfVectorizer(analyzer='word', stop_words='english', use_idf=True)
    tfIdf = tfIdfVectorizer.fit_transform(data_lemmatized)

    top_words = []
    for i in range(len(data_lemmatized)):
        df_tfidf = pd.DataFrame(tfIdf[i].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=['TF-IDF'])
        df_tfidf = df_tfidf.sort_values('TF-IDF', ascending=False)
        print(" TF-IDF - cluster n°{} : \n\n {}".format(i, df_tfidf.head(5)))
        tf_idf_dict = {
            'cluster': i,
            'top_words': df_tfidf.head(5).index.tolist()
        }
        top_words.append(tf_idf_dict)

    output = pd.DataFrame(top_words)
    Path('top_words.csv').touch()
    output.to_csv("top_words.csv")


if __name__ == "__main__":
    print("tf_idf ...")
    parser = argparse.ArgumentParser()
    parser.add_argument('--documents_path')
    args = parser.parse_args()
    tf_idf(args.documents_path)
    print("tf_idf done.")
