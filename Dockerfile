FROM python:3

RUN apt-get update && apt-get -y install cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.daily/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.daily/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD ["cron", "tail", "-f", "/var/log/cron.log"]


ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code/
CMD ["cron", "-f"]