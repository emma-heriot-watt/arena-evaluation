#!/bin/bash

mkdir -p storage/data/trajectory-data

unset AWS_PROFILE
aws s3 cp s3://alexa-simbot-toolbox-iad-prod/simbot-data/action-model/train.json ./storage/data/trajectory-data/train.json
aws s3 cp s3://alexa-simbot-toolbox-iad-prod/simbot-data/action-model/valid.json ./storage/data/trajectory-data/valid.json
aws s3 cp s3://alexa-simbot-toolbox-iad-prod/simbot-data/action-model/T2_valid.json ./storage/data/trajectory-data/T2_valid.json

mkdir -p storage/data/cdfs

aws s3 cp s3://alexa-simbot-toolbox-iad-prod/simbot-data/action-model/T2_CDFs.zip storage/data/cdfs/T2_CDFs.zip
unzip ~/AlexaSimbotToolbox/data/CDFs/T2_CDFs.zip -d storage/data/cdfs/
