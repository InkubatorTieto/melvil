FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
RUN mkdir /code
WORKDIR /code
RUN apt-get update ; apt-get -y upgrade
RUN apt-get -y install libldap2-dev libsasl2-dev
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD proper_ldap_file.py /code
RUN mv proper_ldap_file.py /usr/local/lib/python3.6/site-packages/ldap/filter.py
RUN ls -l /usr/local/lib/python3.6/site-packages/ldap/
ADD . /code/
