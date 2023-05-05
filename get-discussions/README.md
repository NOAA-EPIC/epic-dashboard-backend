# get-discussions Lambda

This AWS Lambda function gets discussions and issues from GitHub via the [GitHub GraphQL API](https://docs.github.com/en/graphql) (or DynamoDB in the case of the top level ufs-community discussions).

Issues and discussions from the following organizations and repositories are supported:
* [ufs-community organization](https://github.com/ufs-community)
* [ufs-community/ufs-srweather-app](https://github.com/ufs-community/ufs-srweather-app)
* [NOAA-EMC/UPP](https://github.com/NOAA-EMC/UPP)

## Environment variables

The following environment variables are required to be defined for the AWS Lambda function:
* `GITHUB_TOKEN` - The GitHub token to use for pulling the issues and discussions data from the GitHub GraphQL API
* `EPIC_BUCKET` - The AWS S3 bucket name of the bucket to store the data in
* `DYNAMO_TABLE_NAME` - The AWS DynamoDB table name of the table where the ufs-community Discussions data is stored

## Commands

Reference the Makefile for supported commands.