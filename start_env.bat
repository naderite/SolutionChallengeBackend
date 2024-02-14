@echo off
cd /d venv\Scripts\
call activate
cd /d ../..
start cmd /k "python manage.py runserver"  
start cmd /k "cd /d ./modelAPI && uvicorn main:app --reload --host 127.0.0.1 --port 8001"  
start cmd /k "ngrok start --all --config=C:\Users\2003n\AppData\Local\ngrok\ngrok.yml"