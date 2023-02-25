#!/bin/sh
if [ ! -d /data ]; then
	mkdir /data
fi

if [ -d /app ]; then
	mv /app/data/config.json /data/config.json
	mv /app/data/pasts.txt /data/pasts.txt
fi
 
python3 ./bot.py
