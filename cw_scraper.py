from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json


class CW_Automation():

    def __init__(self, data):
        """Parameter initialization"""

        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        # self.driver = webdriver.Firefox(executable_path=data['geckodriver_path'])
        # self.driver = webdriver.Chrome(executable_path=data['chromedriver_path'])
        self.driver = webdriver.Chrome(data['driver_path'])
        self.login_cw()

    def login_cw(self):
        """Login to CW Jobs"""
        self.driver.get("https://www.cwjobs.co.uk/account/signin?")

        try:
            # introduce email and password and hit enter
            login_email = self.driver.find_element(By.ID, 'Form_Email')
            login_email.clear()
            login_email.send_keys(self.email)
            login_password = self.driver.find_element(By.ID, 'Form_Password')
            login_password.clear()
            login_password.send_keys(self.password)
            accept_cookies = self.driver.find_element(
                By.ID, 'ccmgt_explicit_accept')
            accept_cookies.click()
            login_button = self.driver.find_element(By.ID, 'btnLogin')
            login_button.click()

            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")

    def job_search(self):
        """Search for jobs"""

        time.sleep(2)
        search_keywords = self.driver.find_element(
            By.XPATH, '//*[@id="keywords"]')
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        time.sleep(1)
        search_location = self.driver.find_element(
            By.XPATH, '//*[@id="location"]')
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(1)
        search_button = self.driver.find_element(
            By.XPATH, '//*[@id="search-button"]')
        search_button.click()
        time.sleep(2)

    def find_offers(self):
        # find the total number of pages of search results
        num_pages = int(self.driver.find_element(
            By.CLASS_NAME, "resultlist-17jh0r6").text)

    # create an empty list to store job posting URLs
        job_links = []

    # Loop through all pages of search results // uncomment code below if you want to scrape all pages
    #     for i in range(1, num_pages + 1):
    #     # navigate to the current page of search results
    #         if i > 1:
    #             self.driver.get(self.driver.current_url + f"&page={i}")

    # Find all the job links on the current page and append them to the job_links list
        job_elements = self.driver.find_elements(
            By.CSS_SELECTOR, '.job-title > a')
        for element in job_elements:
            job_links.append(element.get_attribute('href'))

        # Find all the job links on the current page and append them to the job_links list // in case you want to scrape all pages
        # job_links.extend([link.get_attribute("href") for link in self.driver.find_elements(By.CSS_SELECTOR, ".job__title > a")])

    # write the job links to a text file
        with open("job_links.txt", "w") as f:
            for link in job_links:
                f.write(link + "\n")
                print(f"{len(job_links)} job links saved to job_links.txt")
            


if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)
        bot = CW_Automation(data)
        bot.job_search()
        bot.find_offers()
