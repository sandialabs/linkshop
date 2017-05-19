#!/bin/bash
if [ "$*" == "" ]
then
    echo "usage:"
    echo "  $0 <file>"
    echo "  will read <file>.dot and produce <file>.svg"
    exit 0
fi
unflatten -l6 -o ${1}-unflat.dot ${1}.dot
dot -Tsvg ${1}-unflat.dot > $1.svg
