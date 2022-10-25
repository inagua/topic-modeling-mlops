FROM python:3.8-slim

WORKDIR /app

RUN pip install -U spacy numpy pandas

COPY embeddings.py ./embeddings.py

ENTRYPOINT ["python", "embeddings.py"]