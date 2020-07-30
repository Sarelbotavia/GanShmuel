FROM python:3.6.9
#FROM python:2.7.18

#libmysqlclient-dev python3.7-dev\
RUN apt-get update -y && apt-get install -y apt-utils python3.7-dev libmariadb-dev \ 
    python2.7-dev default-libmysqlclient-dev libssl-dev

RUN pip install --upgrade pip setuptools
RUN pip install flask-mysql flask flask-mysqldb
RUN pip install requests
RUN pip install pandas
RUN export FLASK_APP=app.py
RUN export FLASK_ENV=development
COPY . /