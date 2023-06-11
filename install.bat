@echo off

rem Install Django
pip install django

rem Install core
cd core
python setup.py install
cd ..

rem Install rdf_loader
cd rdf_loader
python setup.py install
cd ..

rem Install xml_loader
cd xml_loader
python setup.py install
cd ..

rem Install json_loader
cd json_loader
python setup.py install
cd ..

rem Install simple_visualizer
cd simple_visualizer
python setup.py install
cd ..

rem Install complex_visualizer
cd complex_visualizer
python setup.py install
cd ..

echo All installations completed.