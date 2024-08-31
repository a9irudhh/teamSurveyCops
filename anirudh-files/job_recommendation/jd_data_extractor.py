import pandas as pd
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from bs4 import BeautifulSoup
import json

def init_driver(path):
    """Initialize the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    service = webdriver.chrome.service.Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def open_browser(driver, locid, key):
    """Open the Glassdoor job search page for the specified location and keyword."""
    query = '+'.join(key.split())
    url = f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={query}&locT=C&locId={locid}&jobType=fulltime&fromAge=1&radius=6"
    driver.get(url)

def get_job_urls(driver, num_urls=20):
    """Collect job URLs from the search results."""
    urls = set()
    while len(urls) < num_urls:
        soup = BeautifulSoup(driver.page_source, "lxml")
        job_listings = soup.find_all("li", {"class": "jl"})
        for listing in job_listings:
            url = f"https://www.glassdoor.co.in{listing.find('a')['href']}"
            urls.add(url)
        try:
            next_button = driver.find_element_by_class_name("next")
            next_button.click()
            time.sleep(2)
        except (NoSuchElementException, ElementClickInterceptedException):
            break
    return list(urls)

def extract_job_details(driver, url):
    """Extract job details from the given job URL."""
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    try:
        job_details = {
            "url": url,
            "Position": driver.find_element_by_tag_name('h2').text,
            "Company": driver.find_element_by_xpath("//span[@class='strong ib']").text,
            "Location": driver.find_element_by_xpath("//span[@class='subtle ib']").text,
            "Job_Description": driver.find_element_by_id("JobDescriptionContainer").text,
        }
        print("Extracted data is as follows:\n{job_details}")
        return job_details
    except NoSuchElementException:
        return None

def scrape_jobs(driver, urls):
    """Scrape job details from a list of URLs."""
    job_data = []
    for url in tqdm(urls, desc="Scraping job details"):
        details = extract_job_details(driver, url)
        if details:
            job_data.append(details)
    return pd.DataFrame(job_data)

def save_data_to_csv(data, path):
    """Save the scraped job data to a CSV file."""
    data.to_csv(path, index=False)
    print(f"Data saved to {path}")

# Main script execution
if __name__ == "__main__":
    chromedriver_path = r'/usr/local/bin/chromedriver-linux64/chromedriver'
    driver = init_driver(chromedriver_path)

    # Step 1: Open browser and search for jobs
    open_browser(driver, locid=4477450, key='"Data Scientist"')

    # Step 2: Get job URLs
    job_urls = get_job_urls(driver, num_urls=20)

    # Step 3: Save job URLs to a JSON file
    with open('url_data_scientist_loc_bangalore.json', 'w') as f:
        json.dump(job_urls, f, indent=4)

    # Step 4: Scrape job details from URLs
    job_data_df = scrape_jobs(driver, job_urls)

    # Step 5: Save job details to a CSV file
    save_data_to_csv(job_data_df, r'./job_data_scientist_loc_bangalore.csv')

    # Quit the driver
    driver.quit()
