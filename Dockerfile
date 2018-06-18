FROM python:3

RUN apt-get update && apt-get -y install cron

# Add crontab file in the cron directory
#ADD crontab /etc/crontab


RUN echo "* * * * * root echo "Hello world" >> /var/log/cron.log" >> /etc/crontab


#RUN echo "* * * * * root echo "Hello world" >> /var/log/cron.log" >> /etc/crontab
# Give execution rights on the cron job
#RUN chmod 777 /etc/crontab

# Create the log file to be able to run tail
#RUN touch /var/log/cron.log
#RUN echo "* * * * * root echo "Hello world" >> /var/log/cron.log" >> /etc/crontab
# Run the command on container startup
#CMD ["cron"]
#CMD ["cron", "tail", "-f", "/var/log/cron.log"]
# Setup cron job
#RUN echo "* * * * * root echo "Hello world" >> /var/log/cron.log" >> /etc/crontab

# Run the command on container startup
#CMD touch /var/log/cron.log && cron && tail -f /var/log/cron.log
#COPY crontab /etc/cron.d/cool-task
#RUN chmod 0644 /etc/cron.d/cool-task
#RUN service cron start

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code/
#CMD cron && tail -F /var/log/cron.log
CMD touch /var/log/cron.log && cron && tail -f /var/log/cron.log