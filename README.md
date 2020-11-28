# Script some control on Sonos speakers

Main reason for this script: Two things I totally miss with Sonos speakers.

## Thing 1: Morning Alarm cannot create a group with all speakers

Totaly unclear to me, why such a feature is not part of the Alarm function in Sonos.

So the script `lambda_function.py` can be scheduled as an AWS Lambda function, triggered via Cloudwatch to run every day an hour or so before the scheduled alarm.

Create AWS Lambda environment variables for the following:

* `client_key` with the client key you received after the OAuth login
* `client_secret` with the client secret you received after the OAuth login
* `refresh_token` with the refresh-token you received after the OAuth login

Schedule and have fun.

## Thing 2: Kids control with hardware-tokens like the Tonies

tbd.
