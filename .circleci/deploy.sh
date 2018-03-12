#!/usr/bin/env bash
set -eo pipefail

install_dependencies() {
	apt-get -y -qq update
	apt-get -y install python-pip python-dev build-essential
	pip install awscli --upgrade
}

create_resource_group() {
	RESOURCE_QUERY='{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"Project\",\"Values\":[\"'"${PROJECT_NAME}"'\"]}]}"}'
	{
		aws resource-groups update-group-query \
			--group-name ${PROJECT_NAME} \
			--resource-query ${RESOURCE_QUERY} \
			--region "us-east-1"
	} || {
		aws resource-groups create-group \
			--name ${PROJECT_NAME} \
			--description "${PROJECT_DESCRIPTION}" \
			--resource-query ${RESOURCE_QUERY} \
			--region "us-east-1"
	}
}

deploy_lambda_function() {
	aws lambda create-function \
		--function-name ${PROJECT_NAME} \
		--role ${LAMBDA_ROLE_ARN} \
		--handler handler \
		--runtime python2.7 \
		--tags Project=${PROJECT_NAME}
}

install_dependencies
create_resource_group
deploy_lambda_function