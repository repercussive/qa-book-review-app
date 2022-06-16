#!/bin/bash
echo "--- Preparing to run app ---"
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

echo "--- Activating venv ---"
python3 -m venv venv
source venv/bin/activate

echo "--- Installing dependencies ---"
pip3 install -r requirements.txt

echo "--- Killing existing processes ---"
kill $(cat gunicornpidfile)

echo "--- Running app ---"
python3 -m gunicorn -D --workers 4 --bind 0.0.0.0:5000 app:app -p gunicornpidfile