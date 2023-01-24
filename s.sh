#! /bin/bash

# echo $SERVICE
# if ps ax | grep -v grep | grep $SERVICE > /dev/null
if ps ax | grep -v grep | grep gunicorn > /dev/null
then
	echo "@SERVICE service running, everything is fine"
else
	echo "@SERVICE is not running"
fi