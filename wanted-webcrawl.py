from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import csv

# Set up the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Go to the webpage
driver.get('https://www.jumpit.co.kr/search?sort=relation&keyword=인공지능')

# Scroll and load more job postings
SCROLL_PAUSE_TIME = 1.5

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

# # Parse the page source with BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# # Close the Selenium WebDriver
# driver.quit()

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
     
