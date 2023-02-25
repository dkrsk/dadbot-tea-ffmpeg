#!/bin/sh
if [ ! -d /data ]; then
	mkdir /data
fi

if [ ! -d /app ]; then
	mv ./config.json /data/config.json
	mv ./pasts.txt /data/pasts.txt
else
	mv /app/config.json /data/config.json
	mv /app/pasts.txt /data/pasts.txt
fi
 
python3 ./bot.py
