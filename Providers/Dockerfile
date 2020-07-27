FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
RUN apt-get install -y python3-flask

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

RUN chmod +x /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN set FLASK_APP=app.py
 
RUN export FLASK_APP=app.py

ENTRYPOINT flask run
