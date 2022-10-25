FROM python:3.8-slim

WORKDIR /app

RUN pip install -U scikit-learn yellowbrick numpy

COPY find_optimal_k_cluster.py ./find_optimal_k_cluster.py

ENTRYPOINT ["python", "find_optimal_k_cluster.py"]