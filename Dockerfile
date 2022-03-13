FROM python:3.9

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ENV PYTHONPATH /app

RUN apt-get -y update
RUN apt-get -y upgrade

COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt