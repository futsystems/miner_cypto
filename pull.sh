#!/bin/bash

git pull

SERVICE=django_chia

echo -e "Restart Service"

supervisorctl  restart django_chia
supervisorctl  restart celery_beat
supervisorctl  restart celery_worker