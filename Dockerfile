# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN pip install -r api/requirements.txt
RUN pip install -r client/requirements.txt
EXPOSE 5000