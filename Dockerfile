FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /megano

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY diploma-frontend .
COPY megano .
