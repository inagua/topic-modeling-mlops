FROM python:3.8-slim

WORKDIR /app

RUN pip install -U scikit-learn numpy

COPY pca.py ./pca.py

ENTRYPOINT ["python", "pca.py"]