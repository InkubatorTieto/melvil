FROM python:3.7-slim

RUN apt-get update && \
    apt-get --assume-yes install cron libpq-dev gcc

RUN mkdir /app
COPY update_reservation_status.py data_access_layer.py requirements.txt /app/
COPY cron /etc/cron.d/
RUN crontab /etc/cron.d/cron

WORKDIR /app
RUN pip install -r requirements.txt

CMD ["cron", "-f"]
