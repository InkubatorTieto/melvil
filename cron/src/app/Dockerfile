FROM python:3.7-slim

RUN apt-get update && \
    apt-get --assume-yes install cron libpq-dev gcc

RUN mkdir /app
COPY update_reservation_status.py data_access_layer.py requirements.txt /app/
COPY cron /etc/cron.d/

WORKDIR /app
RUN pip install -r requirements.txt
RUN mkfifo /var/log/cron.log

CMD cron && tail -f /var/log/cron.log