import json
import boto3
import github_util
import os
from boto3.dynamodb.conditions import Key


def write_data_to_s3(data, key):
    # Initialize the S3 client
    s3 = boto3.client('s3')
    
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
    dynamodb = boto3.resource('dynamodb')
    db = dynamodb.Table(os.environ['DYNAMO_TABLE_NAME'])
    all_ufs_community_discussions = db.query(KeyConditionExpression='repository=:repository',ExpressionAttributeValues={':repository':'ufs-community'})
    
    # Convert the JSON object to a string
    my_data_str = json.dumps(all_ufs_community_discussions['Items'])
    print(my_data_str)
    response = write_data_to_s3(my_data_str, 'discussion-data.json')
    
    all_srw_discussions = github_util.getGitHubDiscussions('ufs-community', 'ufs-srweather-app')
    response = write_data_to_s3(all_srw_discussions, 'discussion-srw-data.json')
    
    all_srw_issues = github_util.getGitHubIssues('ufs-community', 'ufs-srweather-app')
    response = write_data_to_s3(all_srw_issues, 'issue-srw-data.json')

    all_upp_discussions = github_util.getGitHubDiscussions('NOAA-EMC', 'UPP')
    response = write_data_to_s3(all_upp_discussions, 'upp-data.json')

    all_upp_issues = github_util.getGitHubIssues('NOAA-EMC', 'UPP')
    response = write_data_to_s3(all_upp_issues, 'upp-data.json')
    
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
