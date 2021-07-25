#!/bin/bash
git fetch
git reset --hard origin/main
sudo chmod +x flask.sh
sudo chmod +x update.sh
sudo chmod +x app.py
sudo systemctl restart dashboard
