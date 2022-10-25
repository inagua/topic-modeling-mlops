FROM python:3.8-slim

WORKDIR /app

RUN pip install -U scikit-learn numpy

COPY kmeans.py ./kmeans.py

ENTRYPOINT ["python", "kmeans.py"]