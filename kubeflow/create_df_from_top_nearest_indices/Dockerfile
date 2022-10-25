FROM python:3.8-slim

WORKDIR /app

RUN pip install -U pandas numpy

COPY create_df.py ./create_df.py

ENTRYPOINT ["python", "create_df.py"]
