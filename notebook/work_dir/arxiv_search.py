# filename: arxiv_search.py

import requests
import feedparser

# Define the base url and the search query
base_url = 'http://export.arxiv.org/api/query?'
search_query = 'all:trust calibration in AI based systems'

# Send a GET request to the arXiv API and parse the response
response = requests.get(base_url, params={'search_query': search_query})
feed = feedparser.parse(response.content)

# Print the title, authors, and summary of each paper
for entry in feed.entries:
    print('Title: ', entry.title)
    print('Authors: ', ', '.join(author.name for author in entry.authors))
    print('Summary: ', entry.summary)
    print('\n')