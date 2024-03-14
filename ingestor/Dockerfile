FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /home/ingestor

COPY ingestor .
COPY .env .
COPY shared shared

RUN pip install -r requirements.txt

CMD ["python", "ingestion.py"]
