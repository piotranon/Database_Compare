# Dockerfile
# pull official base image
FROM python:3.9-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install musl-dev -y
RUN apt-get install wget -y


# install dependencies
RUN pip install --upgrade pip
RUN pip install Django
RUN pip install django-cors-headers
# RUN pip install -r requirements.txt

RUN pip install requests
RUN pip install clickhouse-driver
RUN pip install psycopg2-binary
RUN pip install pymssql
RUN pip install pandas
RUN pip install django-cors-headers