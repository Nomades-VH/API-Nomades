#!/bin/bash

git pull
mv nomades.service.example /etc/systemd/system/nomades.service
venv/bin/pip install -r requirements.txt
docker-compose down
docker-compose up
systemctl daemon-restart nomades
/home/ubuntu/Nomades-VH/venv/bin/python /home/ubuntu/Nomades-VH/main.py