#! /bin/sh
set -e
echo "apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers mariadb-dev python3-dev"
apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers
echo "pip install mysqlclient"
pip install pipreqs
pipreqs /app
pip install -r /app/requirements.txt
#pip install mysqlclient flask flask-mysqldb pipreqs
echo "apk del .build-deps"
apk del .build-deps
pip unistall pipreqs
#apk add --no-cache mariadb-client-libs
#apk add --no-cache mariadb-client