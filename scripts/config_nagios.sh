#!/bin/bash

wget http://$1.gateway.marvelsystem.net:8080/config/nagios -O /etc/icinga2/zones.d/master/plotter-$1.conf

service icinga2 restart