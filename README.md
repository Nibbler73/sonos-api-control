# Script some control on Sonos speakers

Main reason for this script: Two things I totally miss with Sonos speakers.

## Thing 1: Morning Alarm cannot create a group with all speakers

Totaly unclear to me, why such a feature is not part of the Alarm function in Sonos.

So the script `lambda_function.py` can be scheduled as an AWS Lambda function, triggered via Cloudwatch to run every day an hour or so before the scheduled alarm.

### Installation

#### Prerequisited

A Linux based system with Python3, AWS-CLI, GIT and ZIP installed.

#### The steps

Fetch the repository and install the dependencies

```shell
git clone https://github.com/Nibbler73/sonos-api-control.git
```

Fetch dependencies and ZIP them

```shell
pip3 install --target ./package --system requests
cd package
zip -r9 ../function.zip .
cd ..
```

Add the script to the dependency zip:

```shell
zip -g function.zip lambda_function.py
```

Send the whole package to AWS Lambda

```shell
aws lambda update-function-code --function-name SonosCreateGroup --zip-file fileb://function.zip
```


Create AWS Lambda environment variables for the following:

* `client_key` with the client key you received after the OAuth login
* `client_secret` with the client secret you received after the OAuth login
* `refresh_token` with the refresh-token you received after the OAuth login

Schedule and have fun.

## Thing 2: Kids control with hardware-tokens like the Tonies

tbd.
