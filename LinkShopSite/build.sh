#!/bin/bash
# Build script for compiling and installing all dependancies to set up the 
# environment for Linkshop.

# handle all configurable options
while getopts lpgi option
do
        case "${option}"
        in
		l) LOCAL=true;;
		g) GENKEYS=true;;
		i) IPTABLES=true;;
        esac
done

if [ $IPTABLES ]
then
	sudo apt-get install iptables
	sudo iptables -F
	sudo iptables -A INPUT -p tcp -s 127.0.0.1 --dport 9090 -j ACCEPT
	sudo iptables -A INPUT -p tcp --dport 9090 -j DROP
fi

if [ $GENKEYS ]
then
	# Installing a self signed certificate for the website on the server
	echo "Generating a self signed certificate..."
	openssl req -new -newkey rsa:2048 -nodes -keyout apache-conf/server.key -out apache-conf/server.csr
	openssl x509 -req -days 365 -in apache-conf/server.csr -signkey apache-conf/server.key -out apache-conf/server.crt
	echo "Self signed certificate signed, sealed, and delivered!"
	sudo cp apache-conf/linkshop.crt /etc/ssl/certs
	sudo cp apache-conf/linkshop.key /etc/ssl/private
fi

if [ ! $LOCAL ] 
then
	# Installing all necessary files 
	# If the proxy exists, this must be globally set ahead of time
	echo "Checking for existence of environment dependancies and installing if missing..."

	# Handling for dependancies
	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
	echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
	sudo apt-get update
	sudo apt-get install libboost-dev libboost-test-dev libboost-program-options-dev libboost-system-dev libboost-filesystem-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev
	sudo apt-get install thrift-compiler
	sudo apt-get install npm
    sudo apt-get install krb5-user
    sudo cp apache-conf/krb5.conf /etc/krb5.conf
	sudo apt-get install python-all python-all-dev python-all-dbg python-pip python3-pip python3-numpy
    sudo apt-get install -y mongodb-org
	sudo service mongod stop
	sudo apt-get install apache2 libapache2-mod-proxy-html
	echo "Installing required apache2 modules"
	sudo a2enmod proxy
	sudo a2enmod proxy_http
	sudo a2enmod proxy_ajp
	sudo a2enmod rewrite
	sudo a2enmod deflate
	sudo a2enmod headers
	sudo a2enmod proxy_balancer
	sudo a2enmod proxy_connect
	sudo a2enmod proxy_html
	sudo a2enmod ssl
	sudo cp apache-conf/linkshop.conf /etc/apache2/sites-available/linkshop.conf
	sudo a2ensite linkshop
        sudo a2dissite 000-default.conf
	sudo service apache2 stop
	echo "Performing pip installations..."
	# Perform installations requiring pip 
	sudo pip3 install ../linkograph/ahoCorasick/
	sudo pip3 install thriftpy
        sudo pip3 install pymongo
fi

# Handling for Node.js external library dependancies. These are defined in package.json
echo "Checking for existence of Node.js dependancies..."
if [ ! -d middlewares/node_modules ] 
then
	echo "Installing dependancies for the Node.js files via npm..."
	sudo npm config set registry "http://registry.npmjs.org/"
	sudo npm install
	sudo mv node_modules middlewares/
fi

# Handling for thrift linking files. These are defined in middlewares/thrift.
echo "Checking for existence of thrift linking files..."
if [ ! -d middlewares/thrift/gen-nodejs ] 
then
	echo "Generating thrift linking files..."
	sudo thrift --gen js:node middlewares/thrift/link.thrift
	sudo mv gen-nodejs middlewares/thrift/
fi

echo "Finished!"
