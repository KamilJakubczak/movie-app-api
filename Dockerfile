FROM python:3.8-alpine
MAINTAINER Kamil Jakubczak

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update postgresql-client
RUN apk add --update gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user



