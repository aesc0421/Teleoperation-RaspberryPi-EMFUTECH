#!/bin/bash

# Guarda paquetes apt instalados
dpkg --get-selections > apt-packages.list

# Guarda paquetes pip instalados
pip3 freeze > pip-packages.txt

# Crea un script para reinstalar
cat << 'EOF' > reinstall_env.sh
#!/bin/bash
set -e

echo "Restaurando paquetes APT..."
sudo apt update
sudo apt install -y $(cat apt-packages.list | awk '{print $1}')

echo "Restaurando paquetes PIP..."
pip3 install -r pip-packages.txt

echo "Restauración completa."
EOF

chmod +x reinstall_env.sh

echo "🎉 Archivos generados: apt-packages.list, pip-packages.txt, reinstall_env.sh"
