FROM python:3.6.9-slim-stretch
RUN apt-get update -y && apt-get install -y apt-utils libmariadb-dev libssl-dev
RUN pip install --upgrade pip
RUN pip install pipreqs
COPY . /app
RUN pipreqs --force /app
RUN pip install -r /app/requirements.txt


CMD ["python", "./app.py"]