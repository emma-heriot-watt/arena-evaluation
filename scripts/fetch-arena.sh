#!/bin/bash

mkdir -p storage/arena

unset AWS_PROFILE
aws s3 cp s3://alexa-simbot-toolbox-iad-prod/arena-executable/SimbotChallenge.zip /tmp/
unzip /tmp/SimbotChallenge.zip -d ./storage/arena
rm -f /tmp/SimbotChallenge.zip
