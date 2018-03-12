#!/usr/bin/env bash
set -eo pipefail

RESOURCE_QUERY='{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"Project\",\"Values\":[\"'"${PROJECT_NAME}"'\"]}]}"}'
aws resource-groups update-group-query --group-name ${PROJECT_NAME} --resource-query ${RESOURCE_QUERY} \
|| aws resource-groups create-group --name ${PROJECT_NAME} --resource-query ${RESOURCE_QUERY} --description "${PROJECT_DESCRIPTION}""