# Team 05

## Team members:
- SV07/2020 Savić Anastasija
- SV18/2020 Sladaković Milica
- SV27/2020 Dutina Nemanja
- SV29/2020 Vučić Katarina
- SV32/2020 Adamović Hristina

## Requirements:
- python 3.8 version and higher
- django framework 4.2 version

## Startup instructions:
- position in project package
- create virtual environment -> python -m venv venv
- position in virtual environment -> venv/Scripts/activate
- position in core package -> cd core
- install core plugin -> python setup.py install
- position in wanted plugin package (for example cd../json_loader, ../simple_visualizer)
- install plugin -> python setup.py install
-if you want to uninstall plugin -> pip uninstall [plugin name] (for example pip uninstall json_loader)
- position in core package -> python manage.py runserver

## How to use:
- on the top left corner click button choose file
- after the file is uploaded, choose compatible parser (top left corner)
- now you can choose between simple or complex view (top right corner)
- after this you will be able to see tree view (on the left), graph view (on the right), bird view (on the bottom right corner) and you are able to search and filter (bottom center)

## App is ready to use!