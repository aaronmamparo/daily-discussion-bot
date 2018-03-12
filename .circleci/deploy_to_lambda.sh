#!/usr/bin/env bash
set -eo pipefail

EB_ENV="${PROJECT_NAME}-prod"
eb init "${PROJECT_NAME}" -v -p "Docker 17.09.1-ce" -r "us-east-1"
eb create ${EB_ENV} -v || eb deploy ${EB_ENV} -v
eb tags ${EB_ENV} -v -a Project=${PROJECT_NAME} || eb tags ${EB_ENV} -v -u Project=${PROJECT_NAME}
rm -rf .elasticbeanstalk