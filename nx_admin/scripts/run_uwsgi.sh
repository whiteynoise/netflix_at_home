#!/usr/bin/env bash

set -e

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py add_admin

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini
