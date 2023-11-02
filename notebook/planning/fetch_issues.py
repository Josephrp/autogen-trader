# filename: fetch_issues.py

import requests
import json

def fetch_issues():
    url = "https://api.github.com/repos/microsoft/FLAML/issues"
    response = requests.get(url)
    issues = json.loads(response.text)
    good_first_issues = [issue for issue in issues if 'labels' in issue and any(label['name'] == 'good first issue' for label in issue['labels'])]
    return good_first_issues

def print_issues(issues):
    for issue in issues:
        print(f"Issue Title: {issue['title']}")
        print(f"Issue URL: {issue['html_url']}")
        print(f"Issue Body: {issue['body']}")
        print("\n")

if __name__ == "__main__":
    good_first_issues = fetch_issues()
    print_issues(good_first_issues)