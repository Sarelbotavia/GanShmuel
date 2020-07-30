FROM python:3.6.9-slim-stretch
RUN apt-get update -y && apt-get install -y apt-utils libmariadb-dev libssl-dev 
RUN apt-get update -y && apt-get install -y gcc
RUN pip install --upgrade pip
#RUN pip install pipreqs
COPY . /
#RUN pipreqs --force /app
RUN pip install -r requirements.txt


CMD ["python", "./app.py"]