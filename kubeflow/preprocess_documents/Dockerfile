FROM python:3.8-slim

WORKDIR /app

RUN pip install -U pandas

COPY preprocess_documents.py ./preprocess_documents.py

ENTRYPOINT ["python", "preprocess_documents.py"]
