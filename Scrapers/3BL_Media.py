from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import pandas as pd
import dateparser
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scroll_to_bottom():
    actions = ActionChains(driver)

    # Number of times to send the "End" key
    number_of_times = 3

    # Send the "End" key multiple times
    for _ in range(number_of_times):
        actions.send_keys(Keys.END).perform()

        # Adding a small delay to allow the page to load
        time.sleep(1)


import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start with maximized window

# Initialize the Chrome driver``
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


url = 'https://www.3blmedia.com/news/all'  # Replace with the actual URL

options = ['Environment', 'Green Infrastructure', 'Sustainable Development Goals', 'Sustainable Finance & Socially Responsible Investment']

news = []

for option in options:

    driver.get(url)
    
    # Locate the dropdown element
    dropdown_element = driver.find_element(By.ID, 'edit-field-fmr-primary-category-target-id')

    # Create a Select object
    select = Select(dropdown_element)

    print('Scaraping data for' + option)
    
    # Select the option 
    select.select_by_visible_text(option)
    
    wait = WebDriverWait(driver, 10)

    for i in range(1,2):
        
        time.sleep(5)
        
        response = driver.page_source
    
        soup = BeautifulSoup(response, 'html.parser')
    
        titles = soup.find_all('section', class_='teaser-newsfeed')
        # titles = soup.find_all('div', class_='col-md-9')

        urll = 'https://www.3blmedia.com'

        for title in titles:
            try:
                # print(title)
                heading = title.find('h4', class_='h5 teaser-title').text.strip()
                description = title.text.strip().split('\n')[-1].strip()
                date = title.find('p', class_='date').text.strip()

                link = title.find('h4', class_='h5 teaser-title').span.a['href'] 
                link = urll + link

                image_link = title.find('div', class_='teaser-image').a.img['src']
                image_link = urll + image_link

                news.append([heading, description, date, link, image_link])
            except:
                pass
        
        next_page_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.page-link[rel="next"]')))
        scroll_to_bottom()
        next_page_btn.click()

df_3blmedia = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

date = []
for i in df_3blmedia.itertuples():
    date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

df_3blmedia['Date'] = date

df_3blmedia['Source'] = '3BL Media'

df_3blmedia = df_3blmedia.loc[(df_3blmedia['Date'] >= '2024-06-01')
                     & (df_3blmedia['Date'] <= '2025-12-31')]

df_3blmedia 
