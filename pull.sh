#!/bin/bash

git pull

SERVICE=django_chia

echo -e "Restart Service"

exec supervisorctl  restart django_chia
exec supervisorctl  restart celery_beat
exec supervisorctl  restart celery_worker