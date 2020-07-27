FROM python:2.7.18-alpine3.11
RUN apk update && apk add bash
COPY * /
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install virtualenv
RUN virtualenv venv
RUN export FLASK_APP=app.py
RUN export FLASK_ENV=development
RUN pip install flask-mysql
RUN apk add python2-dev
ENTRYPOINT flask run


