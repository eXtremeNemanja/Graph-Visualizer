# Graph Visualizer

_Project for course Software patterns and components._  
Graph Visualizer is a program that supports custom plugins for graph loading and visualization. Graph loading plugins enable you to load structured file and transform it into graph. Graph visualizers enable you to visualize those graphs.

## Team Members

- [SV 07/2020 - Savić Anastasija](https://github.com/savic-a)
- [SV 18/2020 - Sladaković Milica](https://github.com/coma007)
- [SV 27/2020 - Dutina Nemanja](https://github.com/eXtremeNemanja)
- [SV 29/2020 - Vučić Katarina](https://github.com/kaca01)
- [SV 32/2020 - Adamović Hristina](https://github.com/hristinaina)

## Getting Started

### Python 3.8 or higher

Make sure you have Python 3.8 installed on your system before running this project. You can check your Python version by running the following command:

```bash
python --version
```

Here is a complete guide to install python, if needed: https://docs.python-guide.org/starting/installation/

### Activating the Virtual Environment

To activate the virtual environment using the provided scripts, follow the instructions based on your operating system.

Open a terminal and navigate to the project directory. Then, run the following command:

```bash
chmod +x venv.sh && ./venv.sh  # for macOS and Linux
call   venv.bat                # for Windows
```
Note that, if you have Windows, you need to run these commands from cmd, not integrated terminal.

This will create a new virtual environment named "venv" and activate it in the current command prompt session. 
Once activated, you will see the virtual environment indicator (e.g., (venv)) in your terminal or command prompt, indicating that the virtual environment is active.

### Installation

To install all the packages, run following commands inside venv:

```bash
chmod +x install.sh && ./install.sh  # for macOS and Linux
call   install.bat                   # for Windows
```
Note that, if you have Windows, you need to run these commands from cmd, not integrated terminal.

To check if packages are installed, run following command:

```bash
pip list
```

## Usage

### Running 

To run the app, run followind commands inside venv after installation of plugins:

```bash
chmod +x install.sh && ./install.sh  # for macOS and Linux
call   install.bat                   # for Windows
```
Note that, if you have Windows, you need to run these commands from cmd, not integrated terminal.

To check if packages are installed, run following command:

```bash
chmod +x run.sh && ./run.sh      # for macOS and Linux
call   run.bat                   # for Windows
```
Note that, if you have Windows, you need to run these commands from cmd, not integrated terminal.

### How to use
- on the top left corner click button _Choose File_
- after the file is uploaded, choose compatible parser (_top left corner_)
- after the file is uploaded, choose prefered visualizer (_top right corner_)
- after this you will be able to see tree view (_on the left_), graph view (_on the right_), bird view (_on the bottom right corner_) and you are able to search and filter (_bottom center_)

## App is ready to use!

Happy graphing !
