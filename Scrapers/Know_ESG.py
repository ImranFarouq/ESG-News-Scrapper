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

news= []

driver.get(f'https://www.knowesg.com/environment')
time.sleep(10)
response = driver.page_source
# find_element(By.CLASS_NAME, 'site-main')

# div_blok
soup = BeautifulSoup(response, 'html.parser')
# soup

# div = soup.find('main', 'col-span-10 md:col-span-5 md:ring-offset-1')


titles = soup.find_all('a', 'group py-5 border-b border-neutral-1 block')

url = 'https://www.knowesg.com'

for title in titles:
    try:
        heading = title.find('h2', 'sourceSerif font-normal text-base group-hover:text-primary-dark text-neutral-10 transition-colors duration-100 ease-linear').text.strip()
        date = title.find('div', 'mt-3 text-xs text-neutral-4').text.strip()
        link = title['href']
        link = url + link

        news.append([heading, date, link])
    except Exception as e:
        print(e)
        pass

for i in range(2,10):
    driver.get(f'https://www.knowesg.com/environment/{i}/')
    time.sleep(10)
    response = driver.page_source

    soup = BeautifulSoup(response, 'html.parser')


    titles = soup.find_all('a', 'group py-5 border-b border-neutral-1 block')


    for title in titles:
        try:
            heading = title.find('h2', 'sourceSerif font-normal text-base group-hover:text-primary-dark text-neutral-10 transition-colors duration-100 ease-linear').text.strip()
            date = title.find('div', 'mt-3 text-xs text-neutral-4').text.strip()
            link = title['href']
            link = url + link

            news.append([heading, date, link])
            
        except Exception as e:
            print(e)

df = pd.DataFrame(news, columns=['Title', 'Date', 'Link'])


articles = []


for i in df.itertuples():
    driver.get(i.Link)
    time.sleep(7)
    
    response = driver.page_source

    soup = BeautifulSoup(response, 'html.parser')

    try:
        heading = soup.find('h1', 'font-semibold text-xl sm:text-3xl mt-2 text-neutral-9 leading-8 md:leading-10 lg:leading-10 tracking-wide sourceserif').text

        image_link = soup.find('div', 'gatsby-image-wrapper').picture.img['src']

        date = soup.find('div', 'font-normal text-xs mt-4 text-neutral-4').time.text

        description = soup.find('div', 'mt-9 text-neutral-6 text-lg prose prose-sm 2xl:prose-lg max-w-none tracking-wide sourceserif').h2.text

        articles.append([heading,  description, date, i.Link, image_link])
    except Exception as e:
        print(e)
        pass


df_knnow_Esg = pd.DataFrame(articles, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

date = []
for i in df_knnow_Esg.itertuples():
    date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

df_knnow_Esg['Date'] = date

df_knnow_Esg['Source'] = 'Know ESG'

# df_knnow_Esg = df_knnow_Esg.loc[(df_knnow_Esg['Date'] >= '2024-06-01')
#                      & (df_knnow_Esg['Date'] <= '2025-12-31')]
df_knnow_Esg 
