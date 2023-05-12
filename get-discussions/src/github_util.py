import json
import os
import requests

# Define the GitHub GraphQL API endpoint and authorization token
githubGraphQLendpoint = 'https://api.github.com/graphql'
token = os.environ['GITHUB_TOKEN']

# Define the headers for the GraphQL request
graphQLHeaders = {
    'Authorization': f'Bearer {token}'
}

# Define the GraphQL query
issuesQuery = """
    query ($organization: String!, $repository: String!) {
    repository(owner: $organization, name: $repository) {
        name
        issues(first: 100, orderBy: {field: CREATED_AT, direction: DESC}, states: [OPEN]) {
        totalCount
        nodes {
            createdAt
            number
            title
            updatedAt
            comments(last: 1) {
                totalCount
                nodes {
                    createdAt
                }
            }
            linkedBranches {
                totalCount
            }
        }
        }
    }
    }
    """

discussionsQuery = """
    query ($organization: String!, $repository: String!) {
    repository(owner: $organization, name: $repository) {
        name
        discussions(first: 100, orderBy: {field: CREATED_AT, direction: DESC}, states: [OPEN]) {
        totalCount
        nodes {
            createdAt
            number
            title
            answerChosenAt
            category {
                name
                isAnswerable
            }
            comments(last: 1) {
                totalCount
                nodes {
                    createdAt
                }
            }
        }
        }
    }
    }
    """

def getGitHubIssues(organization, repository):
    variables = {'organization': organization, 'repository': repository}
    response = requests.post(githubGraphQLendpoint, json={'query': issuesQuery, 'variables': variables}, headers=graphQLHeaders)
    data = response.json()
    print(data)
    repository_data = data.get('data', {}).get('repository')

    open_issues = repository_data['issues']['nodes']

    formatted_data = map(lambda x: {
      'repository': repository, 
      'index': x['number'],
      'post_type': 'Issue',
      'github_url': 'https://github.com/' + organization + '/' + repository + '/issues/' + str(x['number']) + '/',
      'initial_answer': 'Yes' if x['comments']['totalCount'] > 0 else 'No',
      'iso_date_time': x['createdAt'],
      'complete_flag': 'No' 
      }, open_issues)
    data = json.dumps(list(formatted_data))
    return data


def getGitHubDiscussions(organization, repository):
    variables = {'organization': organization, 'repository': repository}
    response = requests.post(githubGraphQLendpoint, json={'query': discussionsQuery, 'variables': variables}, headers=graphQLHeaders)
    data = response.json()
    repository_data = data.get('data', {}).get('repository')

    open_issues = filter(lambda issue: issue["answerChosenAt"] == None and 
                                       (issue["category"]["name"] == 'Q&A' or issue["category"]["name"] == 'Ideas'), 
        repository_data['discussions']['nodes'])

    formatted_data = map(lambda x: {
      'repository': repository, 
      'index': x['number'],
      'post_type': 'Discussion',
      'github_url': 'https://github.com/' + organization + '/' + repository + '/discussions/' + str(x['number']) + '/',
      'initial_answer': 'Yes' if x['comments']['totalCount'] > 0 else 'No',
      'iso_date_time': x['createdAt'],
      'complete_flag': 'No' 
      }, open_issues)

    data = json.dumps(list(formatted_data)) 

    return data