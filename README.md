# Bank Management System
Developed by Jayesh Gaikwad

## Stack
HTML5, CSS3, JavaScript, Python, Flask, MongoDB, GitHub, Render.

## Local Run
pip install -r requirements.txt
Copy `.env.example` to `.env`, add your MongoDB URI, then run:
python app.py

## Render
Build command: `pip install -r requirements.txt`
Start command: `gunicorn app:app`
Add `MONGO_URI` and `SECRET_KEY` in Render Environment Variables.

## Important
Use MongoDB Atlas for deployment. Never commit `.env` or real credentials.
