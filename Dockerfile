FROM apache/airflow:slim-2.5.1-python3.8

LABEL org.opencontainers.image.authors="blcksrx@pm.me"

ENV PYTHONUNBUFFERED 0
WORKDIR /home/airflow

COPY ./ ./
USER 0
RUN apt-get update && \
    apt-get install -y  --no-install-recommends  \
    build-essential=12.9 \
    libmysqlclient-dev=8.0.32-1debian11 && \
    chown -R 1000:0 /home/airflow
USER 50000:0

RUN pip3 install -r requirements.txt
