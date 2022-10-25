FROM python:3.8-slim

WORKDIR /app

RUN pip install -U spacy nltk pandas gensim sklearn

COPY tf_idf.py ./tf_idf.py

ENTRYPOINT ["python", "tf_idf.py"]