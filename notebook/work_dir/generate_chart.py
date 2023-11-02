# filename: generate_chart.py

import matplotlib.pyplot as plt

# Define the domains and the number of papers in each domain
domains = ['General', 'Human-Robot Interaction', 'Explainable Robot Systems', 'Computer Vision Applications', '6G Wireless Networks']
num_papers = [5, 1, 1, 1, 1]

# Create a bar chart
plt.bar(domains, num_papers)
plt.xlabel('Domains')
plt.ylabel('Number of Papers')
plt.title('Number of Papers in Each Domain')
plt.xticks(rotation=90)

# Save the chart to a file
plt.savefig('domain_papers.png', bbox_inches='tight')