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


    
news = []

for i in range(1,15):
    try:
        url = f'https://esgmena.com/2024/06/page/{i}'

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        titles = soup.find_all('li', class_='list-post pclist-layout')

        for title in titles:
            
            heading = title.find('h2', 'penci-entry-title entry-title grid-title').text.strip()
            date = title.find('span', 'otherl-date').text.strip()
            try:
                description = title.find('div', 'item-content entry-content').text.strip()
            except:
                description = ''
                
            link = title.find('div', 'thumbnail').a['href']
            image_link = title.find('div', 'thumbnail').a['data-bgset']

            news.append([heading, description, date, link, image_link])

    except Exception as e:
        # print(e)
        pass

df = pd.DataFrame(news, columns=['Title','Description', 'Date', 'Link', 'Image_URL' ])

date = []
for i in df.itertuples():
    date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

df['Date'] = date


df['Source']= 'ESG Mena'


df

