@echo off
CALL .\env\Scripts\activate.bat & python manage.py makemigrations & python manage.py migrate & python manage.py runserver