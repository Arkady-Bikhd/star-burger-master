#!/usr/bin/env bash


set -e

echo $(git pull git@github.com:Arkady-Bikhd/star-burger-master.git);
echo $(apt-get install python3.10-venv);
echo $(/usr/bin/env python3 -m venv venv);
source "./venv/bin/activate";
echo $(/usr/bin/env pip3 install -r requirements.txt);
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo $(/usr/bin/env python3 manage.py collectstatic --noinput);
echo $(/usr/bin/env python3 manage.py migrate --noinput);

systemctl restart postgresql
systemctl restart star_burger
systemctl reload nginx

last_commit_hash=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -d '{"environment": "production","revision": "'$last_commit_hash'","rollbar_name": "capark74","local_username": "root","status": "succeeded"}' \
     -s >/dev/null

echo '������ ������� ��������';