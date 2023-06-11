@echo off

IF EXIST venv (
    echo Removing existing venv...
    rmdir /s /q venv
)

echo Creating new venv...
python -m venv venv

echo Activating venv...
call venv\Scripts\activate

echo venv activated.
