#!/bin/bash

service nomades stop

nohup rm nohup.out

nohup docker-compose stop
nohup docker-compose up &

nohup /home/ubuntu/Nomades-VH/venv/bin/pip install -r requirements.txt

systemctl daemon-reload
service nomades start