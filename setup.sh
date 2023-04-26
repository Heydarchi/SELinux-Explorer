#!/bin/bash
sudo apt install git python3.10 python-is-python3 graphviz python3-pyqt5 python3-pip -y

python -m pip install --upgrade pip 

pip install -r requirements.txt

python -m pip install --upgrade pyqt5