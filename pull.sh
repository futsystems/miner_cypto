#!/bin/bash

git pull

SERVICE=django_chia

echo -e "Restart Service" $SERVICE

exec supervisorctl  restart $SERVICE
