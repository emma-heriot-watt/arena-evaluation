#! /bin/bash

# ------------------ Create the directory for the ML Toolbox ----------------- #
echo "[SimBot] Creating directory for the ML toolbox"
su ubuntu -c 'mkdir -p /home/ubuntu/AlexaSimbotToolbox'
cd /home/ubuntu/AlexaSimbotToolbox || exit 1

# ------------------- Clone the repository for the project ------------------- #
echo "[SimBot] Cloning the ML Toolbox from the emma-simbot/simbot-offline-inference"
su ubuntu -c 'git clone https://github.com/emma-simbot/simbot-offline-inference.git .'

# ---------------------------- Download the arena ---------------------------- #
echo "[SimBot] Downloading the arena"
su ubuntu -c 'sh ./scripts/fetch-arena.sh'

# --------------------------- Install dependencies --------------------------- #
# Copy the files they want us to copy?
sudo cp -r /home/ubuntu/AlexaSimbotToolbox/storage/arena/Dependencies/* /usr/lib/
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

# ------------------------- Install venv with Poetry ------------------------- #
echo "[SimBot] Set up virtual environment"
su ubuntu -c "/home/ubuntu/.local/bin/poetry env use $(/home/ubuntu/.pyenv/bin/pyenv which python)"
su ubuntu -c "/home/ubuntu/.local/bin/poetry install"

# --------------------------- Prepare mission data --------------------------- #
echo "[SimBot] Downloading arena mission data"
su ubuntu -c 'sh ./scripts/fetch-arena-data.sh'

echo "[SimBot] Preparing trajectory data"
su ubuntu -c "/home/ubuntu/.local/bin/poetry run python -m simbot_offline_inference.prepare_trajectory_data"

# ----------------------------------- Done ----------------------------------- #
echo "[SimBot] Done!"
