FROM python:3.8-slim-buster AS django

WORKDIR order_storage

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .