#!/bin/bash
cd /home/Glaceon/Jolteon/dash
source ./venv/bin/activate
python -m pip install -r requirements.txt
python -m gunicorn --certfile=/etc/letsencrypt/live/mcfix.org/fullchain.pem --keyfile=/etc/letsencrypt/live/mcfix.org/privkey.pem -b 0.0.0.0:33000 app:app