#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --username superuser --email superuser@mail.com --password s3*1416u
echo "s3*1416u"
