#! /bin/bash

# ------------------ Create the directory for the ML Toolbox ----------------- #
echo "[SimBot] Creating directory for the ML toolbox"
su ubuntu -c 'mkdir -p /home/ubuntu/AlexaSimbotToolbox'
cd /home/ubuntu/AlexaSimbotToolbox || exit 1

# ------------------- Clone the repository for the project ------------------- #
echo "[SimBot] Cloning the ML Toolbox from the emma-simbot/simbot-ml-toolbox"
su ubuntu -c 'git clone -b t2-inference https://github.com/emma-simbot/simbot-ml-toolbox.git .'

# ---------------------------- Download the arena ---------------------------- #
echo "[SimBot] Downloading the arena executable"
su ubuntu -c 'sh ./scripts/fetch_arena.sh'

# --------------------------- Install dependencies --------------------------- #
# Copy the files they want us to copy?
sudo cp -r /home/ubuntu/AlexaSimbotToolbox/arena/Dependencies/* /usr/lib/
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

# ------------------------ Prepare Python environment ------------------------ #
# echo "[SimBot] Preparing Python environment for T2 inference"
# su ubuntu -c 'pyenv install 3.9'
# su ubuntu -c 'pyenv virtualenv 3.9 ml-toolbox'
# su ubuntu -c 'pyenv local ml-toolbox'
# su ubuntu -c 'pyenv which python; pyenv which pip'
# su ubuntu -c 'pip install flask numpy unityparser opencv-python boto3 scipy pillow jinja2'
# su ubuntu -c 'pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116'

# --------------------------- Prepare mission data --------------------------- #
# echo "[SimBot] Downloading trajectory data"
# su ubuntu -c 'sh ./scripts/fetch_trajectory_data.sh'

# echo "[SimBot] Downloading CDFs data"
# su ubuntu -c 'sh ./scripts/fetch_CDFs.sh'

# echo "[SimBot] Convert trajectory data to the numpy version"

# ----------------------------------- Done ----------------------------------- #
echo "[SimBot] Done!"
