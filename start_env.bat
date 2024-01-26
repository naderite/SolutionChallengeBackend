@echo off
cd /d venv\Scripts\
call activate
cd /d ../..
pip install --upgrade -r requirements.txt
start cmd /k "python manage.py runserver"  
start cmd /k "cd /d ./modelAPI && uvicorn main:app --reload --host 127.0.0.1 --port 8001"  
