#!/bin/bash
# Clean script to remove rebuildable modules

while getopts sl option
do
        case "${option}"
        in
                s) SUSER="sudo";;
				l) LOCAL=true;;
        esac
done

if [ ! $LOCAL ] 
then
	$SUSER rm -r middlewares/node_modules
	$SUSER rm -r middlewares/thrift/gen-nodejs
        #$SUSER rm -r -f /var/lib/mongodb/*
fi
#$SUSER rm models/savedState.json
