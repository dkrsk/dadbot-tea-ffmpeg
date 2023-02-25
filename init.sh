#!/bin/sh
if [ ! -d /data ]; then
	mkdir /data
fi
mv /app/config.json /data/config.json
mv /app/pasts.txt /data/pasts.txt

 
python3 ./bot.py
