import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from bs4 import BeautifulSoup
import json
import time
import random

# Set up the Chrome WebDriver with Service
service = Service('/usr/local/bin/chromedriver-linux64/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(service=service, options=options)

def open_browser(locid, key):
    driver.maximize_window()
    search_query = '+'.join(key.split())
    url = (
        "https://www.glassdoor.co.in/Job/jobs.htm?"
        "suggestCount=0&suggestChosen=true&clickSource=searchBtn&"
        "typedKeyword={}&sc.keyword={}&locT=C&locId={}&jobType=fulltime&fromAge=1&"
        "radius=6&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&companyId=-1&"
        "employerSizes=0&applicationType=0&remoteWorkType=0"
    ).format(search_query, search_query, locid)
    
    driver.get(url)
    return driver

def get_job_urls(driver):
    urls = set()
    while True:
        if len(urls) >= 20:
            break
        soup = BeautifulSoup(driver.page_source, "lxml")
        if not soup:
            print("No soup")

        job_listings = soup.find_all("li", {"class": "JobsList_jobListItem__wjTHv"})
        print(f"Number of job listings found: {len(job_listings)}")

        for job in job_listings:
            link = job.find('a', href=True)
            if link:
                urls.add(link['href'])
        
        print(f"Total job URLs found: {len(urls)}")
        
        next_element = soup.find("li", {"class": "next"})
        if not next_element or not next_element.find('a'):
            break
        
        try:
            driver.find_element(By.CLASS_NAME, "next").click()
            time.sleep(random.uniform(1.5, 3.0))  # Random delay between page clicks
        except (ElementClickInterceptedException, NoSuchElementException):
            break

    return list(urls)

def extract_job_data(urls):
    data = {}
    print(f"Total job URLs to extract data: {len(urls)}")
    for i, url in enumerate(tqdm(urls), start=1):
        try:
            driver.get(url)
            # time.sleep(random.uniform(2, 4))  # Random delay between URL visits
            soup = BeautifulSoup(driver.page_source, "lxml")
            print(f"Extracting data from URL: {url}")
            try:
                position = driver.find_element(By.CLASS_NAME, 'heading_Level1__soLZs').text
                company = driver.find_element(By.CLASS_NAME, 'heading_Heading__BqX5J').text
                location = driver.find_element(By.CSS_SELECTOR, 'div[data-test="location"]').text
                job_description = driver.find_element(By.CSS_SELECTOR, 'div.JobDetails_jobDescription__uW_fK').text
                
                data[i] = {
                    'url': url,
                    'Position': position,
                    'Company': company,
                    'Location': location,
                    'Job_Description': job_description
                }
                
                print(f"Extracted data: {data[i]}")
            except (NoSuchElementException, IndexError):
                print(f"Data not found for URL: {url}")
                continue
        
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    print(f"Total job data extracted: {len(data)}")
    return data

# Main workflow
locid = 4477468
key = "Data Scientist"
driver = open_browser(locid, key)

# Get job URLs and save them to a JSON file
urls = get_job_urls(driver)
with open('./url_data_scientist_loc_noida.json', 'w') as f:
    json.dump(urls, f, indent=4)
    print("URL file created")

# Extract job data and save it to a CSV file
job_data = extract_job_data(urls)
driver.quit()

job_df = pd.DataFrame(job_data).transpose()
job_df = job_df[['url', 'Position', 'Company', 'Location', 'Job_Description']]
job_df.to_csv('./jd_data_scientist_noida.csv', index=False)
print("Job data file created")

# Load and display the data
df1 = pd.read_csv("jd_data_scientist_noida.csv")
print(df1)
