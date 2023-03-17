from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # for set where locate webdriver
from selenium.webdriver.support.ui import WebDriverWait  # to wait for an event
from selenium.webdriver.support import expected_conditions as ec  # special method for waiting until...
from selenium.webdriver.common.by import By  # That's what choices by...


# export PYTHONPATH="${PYTHONPATH}:/1prj/example_beautifulsoup_and_scrapy/"
# https://stackoverflow.com/questions/46074847/selenium-common-exceptions-webdriverexception-message-chromedriver-executabl
# service = Service('chromedriver.exe')  # version 110 # chromedriver.exe for windows chrome (where located webdriver)
service = Service('/1prj/example_beautifulsoup_and_scrapy/selenium/chromedriver')  # vers.111  (where located webdriver)
options = webdriver.ChromeOptions()
options.add_argument('--headless=chrome')  # for work without opening chrome
# options.add_argument('--headless=chromium')  # for work without opening chromium

URL = 'https://quotes.toscrape.com/'

if __name__ == '__main__':  # SELENIUM! example

    with webdriver.Chrome(service=service, options=options) as driver:  # open(start) chrome with webdriver
        driver.get(f'{URL}/login')  # get login page
        # Wait 10 seconds until the input fields appear (field with id='password')
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'password')))  # tuple is locator
        # find method (find_element) take locator(tuple) How will we look for:
        username = driver.find_element(by=By.ID, value='username')
        password = driver.find_element(by=By.ID, value='password')  # some webelements 

        username.send_keys('admin')  # filling field - input 'admin' by method send_keys
        password.send_keys('admin')
        # Find the button to enter (send information entered)
        submit = driver.find_element(by=By.XPATH, value='/html//input[@class="btn btn-primary"]')
        submit.click()  # click the button

        # Wait 10 seconds until the tags-elements appear 
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'tags-box')))
        html = driver.page_source  # download all page
        # print(html)

        links = driver.find_elements(by=By.TAG_NAME, value='a')
        for link in links:
            print(link.get_attribute('href'))

        sleep(3)
