#!/usr/bin/env bash
set -eo pipefail

apt-get -y -qq update
apt-get -y install python-pip python-dev build-essential
pip install awscli awsebcli --upgrade