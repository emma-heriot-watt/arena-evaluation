#! /bin/bash

killServers() {
	echo "===== Shutting down servers ====="
	sudo pkill node
}

trap killServers SIGINT

cd bin/StreamingServerWebRTC || exit 1

npm install
npm run build

sudo iptables -t nat -A PREROUTING -p tcp --dport 81 -j REDIRECT --to-port 8080
sudo iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 81 -j REDIRECT --to-ports 8080

sleep 5

cd ..
npm run start --prefix ./StreamingServerWebRTC -- -p 8080 -w

killServers
