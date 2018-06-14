FROM python:3
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code
