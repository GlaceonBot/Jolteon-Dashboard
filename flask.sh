cd /home/Glaceon/Jolteon/dash
source ./venv/bin/activate
python -m pip install -r requirements.txt
python -m gunicorn -b 0.0.0.0:33000 app:app
