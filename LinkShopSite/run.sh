#!/bin/bash
# This script is responsible for running the LinkShop web interface.

echo "Starting the mongodb service..."
sudo service mongod start

echo "Starting the backend python3 server..."
python3 controllers/linkServer.py &
SERVER=$!
echo "Success!"

echo "Starting the Node.js server..."
nodejs controllers/linkClient.js &
CLIENT=$!

echo "Starting the Apache2 server..."
sudo service apache2 restart

echo "The Linkshop services have started! The PID's of the processes are ${SERVER} and ${CLIENT}."
while [ "${QUIT}" != "q" ]
do
	if [ ! $QUIT ]
	then
		echo "Please press 'q' and the 'enter' key when you would like to exit, otherwise the services will need to be manually killed."
	else
		echo "Invalid input: Please press 'q' and the 'enter' key when you would like to exit."
	fi
	
	read QUIT
done

sudo service apache2 stop
kill $SERVER
kill $CLIENT
sudo service mongod stop

echo "Services killed!"
