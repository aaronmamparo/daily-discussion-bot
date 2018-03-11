#!/usr/bin/env bash
set -eo pipefail

VALID=1
if [[ ! -v AWS_ACCESS_KEY_ID ]]; then echo 'Missing environment variable "AWS_ACCESS_KEY_ID"' && VALID=0; fi;
if [[ ! -v AWS_SECRET_ACCESS_KEY ]]; then echo 'Missing environment variable "AWS_SECRET_ACCESS_KEY"' && VALID=0; fi;
if [[ ! -v PROJECT_NAME ]]; then echo 'Missing environment variable "PROJECT_NAME"' && VALID=0; fi;
if [[ ! -v PROJECT_DESCRIPTION ]]; then echo 'Missing environment variable "PROJECT_DESCRIPTION"' && VALID=0; fi;
if [[ ${VALID} -eq 0 ]]; then exit 1; fi;