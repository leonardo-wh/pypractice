FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /code/
COPY ../Pipfile ./

RUN pip install 'pipenv==2024.4.0'
RUN pipenv install
RUN pipenv install --dev
RUN apt-get update

COPY . /code/

EXPOSE 8000
EXPOSE 6379
EXPOSE 6655
