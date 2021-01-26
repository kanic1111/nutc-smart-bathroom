#!/bin/bash
sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.6

git clone https://github.com/creationix/nvm.git ~/.nvm

source ~/.nvm/nvm.sh

nvm install 10

nvm alias default 10

npm install -g pm2

git clone https://github.com/TitanLi/Brunei-Hackathon.git ~/Brunei-Hackathon

cd ~/Brunei-Hackathon/API/raspberry-pi

npm install

pm2 start app.js --name "API-Service"

cd ~/Brunei-Hackathon/frontend/iot

npm install

pm2 start node_modules/react-scripts/scripts/start.js --name "web-service"

pip3 install -r requirements.txt

pm2 start app.py --interpreter python3 --interpreter-args -u --name "Control-Service"
