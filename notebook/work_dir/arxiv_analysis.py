# filename: arxiv_analysis.py

import requests
import feedparser
import matplotlib.pyplot as plt

def fetch_papers(search_query):
    """
    Fetch papers related to a specific topic from ArXiv.

    Non-coding steps:
    - Formulate the search query based on the topic.

    Args:
    search_query (str): The search query.

    Returns:
    list: A list of dictionaries, each containing the title, authors, and summary of a paper.
    """
    base_url = 'http://export.arxiv.org/api/query?'
    response = requests.get(base_url, params={'search_query': search_query})
    feed = feedparser.parse(response.content)

    papers = []
    for entry in feed.entries:
        paper = {
            'title': entry.title,
            'authors': ', '.join(author.name for author in entry.authors),
            'summary': entry.summary
        }
        papers.append(paper)

    return papers

def generate_chart(domains, num_papers, filename):
    """
    Generate a bar chart of domains and the number of papers in each domain, and save the chart to a file.

    Non-coding steps:
    - Analyze the fetched papers to identify the application domains studied by these papers.

    Args:
    domains (list): A list of domains.
    num_papers (list): A list of the number of papers in each domain.
    filename (str): The name of the file to save the chart to.
    """
    plt.bar(domains, num_papers)
    plt.xlabel('Domains')
    plt.ylabel('Number of Papers')
    plt.title('Number of Papers in Each Domain')
    plt.xticks(rotation=90)
    plt.savefig(filename, bbox_inches='tight')