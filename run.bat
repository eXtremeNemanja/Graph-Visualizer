@echo off

cd core

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

cd ..

