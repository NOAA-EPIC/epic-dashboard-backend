import json
import boto3
import github_util
import os
from boto3.dynamodb.conditions import Key


repositories = [
    { 'organization': 'ufs-community', 'repository': 'ufs-srweather-app' },
    { 'organization': 'ufs-community', 'repository': 'ufs-weather-model' },
    { 'organization': 'ufs-community', 'repository': 'land-DA_workflow' },
    { 'organization': 'NOAA-EPIC', 'repository': 'land-offline_workflow' },
    { 'organization': 'NOAA-EMC', 'repository': 'UPP' }
]

def write_data_to_s3(s3, data, key):
    print('Wrote data to file ' + key)

    # Write the JSON string to S3
    response = s3.put_object(
        Bucket=os.environ['EPIC_BUCKET'],
        Key=key,
        Body=data.encode('utf-8'),
        ACL='public-read'
    )

    return response


def lambda_handler(event, context):
    print(event)

    # Initialize the S3 client
    s3 = boto3.client('s3')

    for repo in repositories:
        discussions = github_util.getGitHubDiscussions(repo['organization'], repo['repository'])
        response = write_data_to_s3(s3, discussions, 'discussions-' + repo['organization'] + "-" + repo['repository'] + ".json")
        issues = github_util.getGitHubIssues(repo['organization'], repo['repository'])
        response = write_data_to_s3(s3, issues, 'issues-' + repo['organization'] + "-" + repo['repository'] + ".json")
    
    return {
        'statusCode': 200,
        "isBase64Encoded": 'false',
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        },
        'body': json.dumps({"Schema exists": {"response_list":"Found all responses"}})
    }