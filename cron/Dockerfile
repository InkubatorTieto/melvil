FROM python:3.7-slim

RUN apt-get update && \
    apt-get --assume-yes install cron libpq-dev gcc

RUN mkdir /app
COPY .flake8 requirements.txt /app/
COPY src /app/src
COPY start_container.sh /bin/
COPY cron_job /etc/cron.d/

RUN chmod 755 /bin/start_container.sh && \
    chmod 755 /etc/cron.d/cron_job

WORKDIR /app
RUN pip install -r requirements.txt

CMD ["start_container.sh"]
