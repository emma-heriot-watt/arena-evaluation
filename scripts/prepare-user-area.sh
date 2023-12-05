#! /bin/bash
set -e
set -o pipefail

# This script prepares the user area for the user to run the offline inference

# Make sure this script is run as sudo
if [ "$EUID" -ne 0 ]; then
	echo "Please run as sudo"
	exit 1
fi

# Ensure python version is 3.9, and fail otherwise
if [[ $(python3 --version) != *"3.9"* ]]; then
	echo "Please use python 3.9."
	exit 1
fi

# Ensure poetry is installed
if ! command -v poetry &>/dev/null; then
	echo "Poetry could not be found"
	exit 1
fi

# Install poetry deps without the experience hub
echo "[SimBot] Installing poetry dependencies"
poetry install --without emma

# Clone the experience hub into the storage dir
echo "[SimBot] Installing experience hub as editable"
git clone https://github.com/emma-heriot-watt/experience-hub storage/experience-hub
pip install -e storage/experience-hub

# Fetch the arena
echo "[SimBot] Fetching the arena"
sh ./scripts/fetch-arena.sh

# Set the permissions for the arena
echo "[SimBot] Set permissions for the arena"
sudo chmod -R 755 storage/arena/Linux
chmod 777 storage/arena/Linux/Arena.x86_64

# Install the arena dependencies by copying the files they want us to copy
echo "[SimBot] Installing arena dependencies"
# Warn the user in bright red
echo -e "\e[1;31m"
echo "WARNING!!!!!!!"
echo "THIS WILL CHANGE FILES ON YOUR MACHINE!!!!!"
echo "EITHER RUN THIS INSIDE A CONTAINER OR BACKUP THAT FOLDER BEFORE YOU RUN THIS."
# Reset the colour
echo -e "\e[0m"
# Ask the user if they want to continue
read -p "Do you want to continue? (y/n) " -n 1 -r

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
	echo
	echo "Aborting."
	exit 1
fi
sudo cp -r storage/arena/Dependencies/* /usr/lib/
sudo ldconfig

# Download the arena data
echo "[SimBot] Downloading arena mission data"
sh ./scripts/fetch-arena-data.sh

# Setup symlinks for Docker and storage/models
echo "[SimBot] Setting up symlinks"
ln -s ./storage/experience-hub/docker/ ./
ln -s ./storage/experience-hub/storage/models/ ./storage/

# Done
echo "[SimBot] Done!"
