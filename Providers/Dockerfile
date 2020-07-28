FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /requirements.txt
COPY ./app.py /app.py

RUN pip install -r requirements.txt
RUN apt install python3-flask -y
RUN pip install flask
RUN pip install flask-mysqldb

RUN set FLASK_APP=app.py

RUN export FLASK_APP=app.py

ENTRYPOINT flask run

