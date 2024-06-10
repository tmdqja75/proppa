import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import csv

from scrapegraphai.graphs import XMLScraperGraph

# Set up the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Go to the webpage
# driver.get('https://www.jumpit.co.kr/search?sort=relation&keyword=인공지능')
driver.get('https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=job.recommend_order&years=-1&selected=1024&selected=1634&locations=all')


# Scroll and load more job postings
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load the page
    time.sleep(SCROLL_PAUSE_TIME)
    
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height



# Parse the page source with BeautifulSoup
page_source = driver.page_source
# Convert to XML
# page_source = page_source.prettify(formatter="xml")

# Close the Selenium WebDriver
driver.quit()

# print(page_source)

with open('page_source.xml', 'w', encoding='utf-8') as file:
    file.write(page_source)

# Define the graph configuration

# ollama configuration
# # from https://www.scrapingbee.com/blog/scrapegraph-ai-tutorial-scrape-websites-easily-with-llama-ai/
# graph_config = {
#     "llm": {
#         "model": "ollama/llama3",  # Specifies the large language model to use
#         "temperature": 0,          # Temperature controls randomness; 0 makes it deterministic
#         "format": "json",          # Output format is set to JSON
#         "base_url": "http://localhost:11434",  # Base URL where the Ollama server is running
#     },
#     "embeddings": {
#         "model": "ollama/nomic-embed-text",  # Specifies the embedding model to use
#         "temperature": 0,                    # Keeps the generation deterministic
#         "base_url": "http://localhost:11434",  # Base URL for the embeddings model server
#     },
#     "verbose": True
# }

# OpenAI configuration
graph_config = {
    "llm": {
        "api_key": os.environ.get('OPENAI_API_KEY'),
        "temperature": 0,
        "format": "json",
        "model": "gpt-4-turbo", 
    },
    # "embeddings": {
    #     "model": "ollama/nomic-embed-text",  
    #     "temperature": 0,                    
    #     "base_url": "http://localhost:11434",
    # },
    "verbose": True
}

graph = XMLScraperGraph(
    prompt='scrape all job posting uri from the given xml file.',
    source=page_source,
    config=graph_config,
)

result = graph.run()
print(result)

# # Extract job links
# job_list = soup.find('ul', {'data-cy': 'job-list'})
# job_links = job_list.find_all('a', {'data-attribute-id': 'position__click'})

# # Base URL for job postings
# base_url = 'https://www.wanted.co.kr'

# # Step 3: Fetch details from each job posting
# job_details = []

# for job_link in job_links:
#     job_url = base_url + job_link['href']
#     job_response = requests.get(job_url)
#     job_soup = BeautifulSoup(job_response.content, 'html.parser')
    
#     # Extract job information (example fields)
#     try:
#         job_title = job_soup.find('h2').text.strip()
#         company_name = job_soup.find('a', {'data-attribute-id': 'company-name'}).text.strip()
#         job_location = job_soup.find('span', {'data-attribute-id': 'location'}).text.strip()
#         job_experience = job_soup.find('span', {'data-attribute-id': 'experience'}).text.strip()
#         job_salary = job_soup.find('span', {'data-attribute-id': 'salary'}).text.strip()
        
#         job_details.append({
#             'Job Title': job_title,
#             'Company Name': company_name,
#             'Location': job_location,
#             'Experience': job_experience,
#             'Salary': job_salary,
#             'Job URL': job_url
     
