#!/bin/bash
set -e

echo "Restaurando paquetes APT..."
sudo apt update
sudo apt install -y $(cat apt-packages.list | awk '{print $1}')

echo "Restaurando paquetes PIP..."
pip3 install -r pip-packages.txt

echo "Restauración completa."
