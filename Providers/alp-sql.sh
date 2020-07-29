#! /bin/sh
set -e
echo "apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers mariadb-dev python3-dev"
apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers
echo "pip install mysqlclient"
pip install -r requirements.txt
echo "apk del .build-deps"
apk del .build-deps
#apk add --no-cache mariadb-client-libs
#apk add --no-cache mariadb-client