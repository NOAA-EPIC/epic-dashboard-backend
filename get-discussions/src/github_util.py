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
            author {
                login
            }
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
            labels(first: 5) {
                nodes {
                    name
                }
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
            author {
                login
            }
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
            labels(first: 5) {
                nodes {
                    name
                }
            }
        }
        }
    }
    }
    """

# datatype = "issues" or "discussions"
def format_data(data, organization, repository, dataType):
    # print(data)

    formatted_data = map(lambda x: {
      'repository': repository, 
      'index': x['number'],
      'post_type': dataType,
      'github_url': 'https://github.com/' + organization + '/' + repository + '/' + dataType + '/' + str(x['number']) + '/',
      'initial_answer': 'Yes' if x['comments']['totalCount'] > 0 else 'No',
      'iso_date_time': x['createdAt'],
      'complete_flag': 'No',
      'last_comment_date_time': x['comments']['nodes'][0]['createdAt'] if x['comments']['totalCount'] > 0 else '',
      'author': x['author']['login'],
      'complete_flag': 'No',
      'labels': [d['name'] for d in x['labels']['nodes']]
      }, data)
    data = json.dumps(list(formatted_data))
    return data


def getGitHubIssues(organization, repository):
    variables = {'organization': organization, 'repository': repository}
    response = requests.post(githubGraphQLendpoint, json={'query': issuesQuery, 'variables': variables}, headers=graphQLHeaders)
    data = response.json()
    print(data)
    repository_data = data.get('data', {}).get('repository')

    data = format_data(repository_data['issues']['nodes'], organization, repository, "issues")
    return data

def getGitHubDiscussions(organization, repository):
    variables = {'organization': organization, 'repository': repository}
    response = requests.post(githubGraphQLendpoint, json={'query': discussionsQuery, 'variables': variables}, headers=graphQLHeaders)
    data = response.json()
    repository_data = data.get('data', {}).get('repository')

    open_issues = filter(lambda issue: issue["answerChosenAt"] == None and 
                                       (issue["category"]["name"] == 'Q&A' or issue["category"]["name"] == 'Ideas'), 
        repository_data['discussions']['nodes'])

    data = format_data(open_issues, organization, repository, "discussions")

    return data
