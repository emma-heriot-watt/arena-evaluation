#!/bin/bash

mkdir -p storage/arena

wget -P ./storage/ "https://alexa-arena-executable.s3.us-west-1.amazonaws.com/Arena.zip"
unzip ./storage/Arena.zip -d ./storage/arena
rm -f ./storage/Arena.zip
