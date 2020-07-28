FROM python:3.6.9-alpine
RUN apk update && apk add mariadb-dev 
RUN pip install --upgrade pip
COPY alp-sql.sh /alp.sh
RUN chmod +x /alp.sh
RUN ./alp.sh
RUN export FLASK_APP=app.py
COPY * /
ENTRYPOINT ["python", "./app.py"]

