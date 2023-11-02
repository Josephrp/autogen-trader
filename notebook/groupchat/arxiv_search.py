# filename: arxiv_search.py
import requests
import feedparser

def get_latest_paper_about_gpt4():
    base_url = 'http://export.arxiv.org/api/query?'
    query = 'GPT-4'
    params = 'search_query=all:{}&sortBy=submittedDate&sortOrder=descending'.format(query)

    response = requests.get(base_url + params)

    if response.status_code == 200:
        # Parse the response
        feed = feedparser.parse(response.content)

        # The 'entries' key contains the info about publications
        entries = feed.entries

        if entries:
            # Grab the info about the latest publication
            latest_paper_title = entries[0]['title']
            latest_paper_summary = entries[0]['summary']
            latest_paper_pdf_link = entries[0]['links'][1]['href']

            print("Title: {}\nSummary: {}\nPDF link: {}".format(latest_paper_title, latest_paper_summary, latest_paper_pdf_link))
        else:
            print("No papers about GPT-4 found.")
    else:
        print("Couldn't fetch data from arxiv.")

get_latest_paper_about_gpt4()