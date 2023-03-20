#!/bin/bash

mkdir -p storage/arena

unset AWS_PROFILE

wget -P /tmp/ "https://alexa-arena-executable.s3.us-west-1.amazonaws.com/Arena.zip"
unzip /tmp/Arena.zip -d ./storage/arena
rm -f /tmp/Arena.zip

# aws s3 cp s3://alexa-simbot-toolbox-iad-prod/arena-executable/SimbotChallenge.zip /tmp/
# unzip /tmp/SimbotChallenge.zip -d ./storage/arena
# rm -f /tmp/SimbotChallenge.zip
