FROM python:3.8-slim

WORKDIR /app

RUN pip install -U pandas

COPY preprocess_input_text.py ./preprocess_input_text.py

ENTRYPOINT ["python", "preprocess_input_text.py"]