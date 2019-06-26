FROM python:3.7-slim

RUN apt-get update && \
    apt-get --assume-yes install cron libpq-dev gcc

RUN mkdir /app
COPY update_reservation_status.py data_access_layer.py requirements.txt test_update_reservation_status.py /app/
COPY start_container.sh /bin/
COPY cron /etc/cron.d/

RUN chmod 755 /bin/start_container.sh

WORKDIR /app
RUN pip install -r requirements.txt

CMD ["start_container.sh"]
