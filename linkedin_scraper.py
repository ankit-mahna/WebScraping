#!/usr/bin/ env python3

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import getpass
import sys
import time

# Login credentials
email_id = "ankitmahna92@gmail.com"
password = getpass.getpass(stream=sys.stderr)

driver = webdriver.Safari()
page = driver.get("https://www.linkedin.com/login")
driver.maximize_window()
# enter_email
driver.find_element_by_xpath('//*[@id="username"]').send_keys(email_id)
# enter_password
enter_password = driver.find_element_by_xpath('//*[@id="password"]')
enter_password.send_keys(password)
enter_password.send_keys(Keys.ENTER)

# find and click search bar
search_bar = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search']")))
search_bar.click()
search_bar.send_keys(Keys.ARROW_DOWN)
search_bar.send_keys(Keys.ARROW_DOWN)
search_bar.send_keys(Keys.ARROW_DOWN)
search_bar.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

# using BeautifulSoup to identify companies button by class
time.sleep(5)
login_page_url = driver.current_url
response = requests.get(login_page_url)
soup = BeautifulSoup(response.text, 'html.parser')
h3_tag = soup.find_all('h3')
