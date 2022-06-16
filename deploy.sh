#!/bin/bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
kill $(cat gunicornpidfile)
python3 -m gunicorn -D --workers 4 --bind 0.0.0.0:5000 app:app -p gunicornpidfile