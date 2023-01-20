#! /bin/bash

ROOT="/home/ubuntu/offline-inference"

# ------------------ Create the directory for the ML Toolbox ----------------- #
echo "[SimBot] Creating directory for the ML toolbox"
su ubuntu -c "mkdir -p $ROOT"
cd $ROOT || exit 1

# ------------------- Clone the repository for the project ------------------- #
echo "[SimBot] Cloning emma-simbot/simbot-offline-inference"
su ubuntu -c 'git clone https://github.com/emma-simbot/simbot-offline-inference.git .'

echo "[SimBot] Cloning emma-simbot/experience-hub"
su ubuntu -c 'mkdir -p storage'
su ubuntu -c "git clone https://github.com/emma-simbot/experience-hub.git ./storage/experience-hub"

# ---------------------------- Download the arena ---------------------------- #
echo "[SimBot] Downloading the arena"
su ubuntu -c 'sh ./scripts/fetch-arena.sh'

echo "[SimBot] Set permissions for the arena"
sudo chmod -R 755 $ROOT/storage/arena/Linux
chmod 777 $ROOT/storage/arena/Linux/SimbotChallenge.x86_64

# --------------------------- Install dependencies --------------------------- #
# Copy the files they want us to copy?
sudo cp -r $ROOT/storage/arena/Dependencies/* /usr/lib/
sudo ldconfig

# Install PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' &&
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - &&
	sudo apt update &&
	sudo apt -y install postgresql

# Install nvm
su ubuntu -c 'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash'

# Activate nvm in current shell and install the right versions
su ubuntu -c 'source /home/ubuntu/.nvm/nvm.sh && nvm install 14.17.5'
su ubuntu -c 'source /home/ubuntu/.nvm/nvm.sh && npm install -g n'
su ubuntu -c "source /home/ubuntu/.nvm/nvm.sh && sudo -E env 'PATH=$PATH' n 14.17.5"

# Install ffmpeg
sudo apt install -y ffmpeg

# --------------------------- Prepare mission data --------------------------- #
echo "[SimBot] Downloading arena mission data"
su ubuntu -c 'sh ./scripts/fetch-arena-data.sh'

# ----------------------------------- Done ----------------------------------- #
echo "[SimBot] Done!"
