FROM python:3.6.9-slim-stretch
RUN apt-get update -y && apt-get install -y apt-utils libssl-dev libcurl4-openssl-dev
RUN apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install pipreqs
COPY . /
RUN pipreqs --force e2e
RUN pip install -r e2e/requirements.txt



#for testing envoirment based on slim :
#apt-get install libssl-dev
#apt-get install libcurl4-openssl-dev