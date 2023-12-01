#!/bin/bash

mkdir -p storage/data/trajectory-data

aws s3 cp s3://alexa-arena-resources/DATA_LICENSE ./storage/data/DATA_LICENSE --no-sign-request
aws s3 cp s3://alexa-arena-resources/data/trajectory-data/valid.json ./storage/data/trajectory-data/valid.json --no-sign-request
