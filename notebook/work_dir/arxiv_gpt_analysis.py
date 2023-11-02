# filename: arxiv_gpt_analysis.py

import requests
import feedparser
import matplotlib.pyplot as plt
from typing import List, Dict
from collections import Counter
import re

def search_arxiv(query: str, max_results: int = 100) -> List[Dict[str, str]]:
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query=all:{query}"
    start = 0
    max_results = f"max_results={max_results}"
    url = f"{base_url}{search_query}&start={start}&{max_results}"
    response = requests.get(url)
    feed = feedparser.parse(response.content)
    
    papers = [{"title": entry.title, "link": entry.link, "summary": entry.summary} for entry in feed.entries]
    return papers

def generate_bar_chart(domains: Dict[str, int], output_file: str) -> None:
    fig, ax = plt.subplots()
    ax.bar(domains.keys(), domains.values())
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Application Domains")
    plt.ylabel("Number of Papers")
    plt.title("Number of Papers per Application Domain")

    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()

# Define application domains
domains = ["natural language processing", "machine translation", "text generation", 
           "question answering", "summarization", "sentiment analysis", "chatbots"]

# Search arxiv for papers related to GPT models
papers = search_arxiv("GPT models")

# Analyze the abstracts of the collected papers to identify application domains
domain_counts = Counter()
for paper in papers:
    for domain in domains:
        if re.search(domain, paper["summary"], re.IGNORECASE):
            domain_counts[domain] += 1

# Generate a bar chart of the application domains and the number of papers in each domain
generate_bar_chart(domain_counts, "gpt_domains.png")