#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
import numpy as np
import pandas as pd

# URL for imdb home page - DO NOT CHANGE
base_url = 'https://www.imdb.com'

# imdb title code for a title
imdb_code = 'tt8579674'

# using selenium to load page and search title
driver = webdriver.Safari()  # creating webdriver object for Safari browser
driver.get(base_url)   # opening up the web page
driver.maximize_window()
search_bar = driver.find_element_by_xpath('//*[@id="suggestion-search"]')  # identifying search bar on the web page
# equivalent of entering the imdb title code and pressing enter
search_bar.send_keys(imdb_code)
search_bar.send_keys(Keys.ENTER)

# giving sleep time so tha the current page url is updated
time.sleep(2)

# extracting current url and its corresponding html
print("Scrapping Web Page: ", driver.current_url)
url = driver.current_url
response = requests.get(url)

# creating a parse tree with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
div_tag = soup.find_all('div', class_ = 'user-comments')
all_reviews_url = base_url + div_tag[0].contents[-2]['href']
response = requests.get(all_reviews_url)
soup_reviews = BeautifulSoup(response.text, 'html.parser')

div_tag_review_page = soup_reviews.find_all('div', class_ = 'lister-list')
review_dict = {}

for n_rev in range(len(div_tag_review_page[0].contents)):
    soup_3 = div_tag_review_page[0].contents[n_rev]
    if soup_3 != '\n':
        try:
            review_score = soup_3.find_all('div', class_ = 'ipl-ratings-bar')[0].span.contents[-3].string.strip()  # Get Review Title
        except:
            review_score = np.nan
        try:
            review_title = soup_3.find_all('a')[0].string.rstrip()  # Get Review Score
        except:
            review_title = np.nan
        try:
            review = soup_3.find_all('div', class_ = 'content')[0].contents[1].text.strip()  # Get Review
        except:
            review = np.nan

        # filling data in review dictionary
        if len(review_dict) == 0:
            review_dict['Review_Title'] = review_dict.get('Review_Title', [review_title])
            review_dict['Review_score'] = review_dict.get('Review_score', [review_score])
            review_dict['Review'] = review_dict.get('Review', [review])
        else:
            review_dict['Review_Title'] += [review_title]
            review_dict['Review_score'] += [review_score]
            review_dict['Review'] += [review]

    else:
        continue

print(len(review_dict['Review']))
driver.close()  # closing web browser

# creating dataframe from dictionary and saving it to csv
all_reviews = pd.DataFrame.from_dict(review_dict)
all_reviews.to_csv('{} reviews.csv'.format(imdb_code))
