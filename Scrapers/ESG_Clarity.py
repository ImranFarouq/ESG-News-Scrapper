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


url = 'https://esgclarity.com/asia/news-asia/'

news = []

for i in range(1,3):
    response = requests.get(url + f'page/{i}/')

    soup = BeautifulSoup(response.content, 'html.parser')

    titles = soup.find_all('div', class_='homepage-article-container')
    # print(titles)

    for title in titles:
        image_link = title.find('div', 'homepage-article-image-container').a.img['src']
        heading = title.find('div', class_='homepage-article-content-container').a.text.strip()
        date = title.find('div', class_='entry-meta').text.strip()
        description = ''
        news.append([heading, description, date , title.a['href'], image_link])

df_esg_clarity = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

date = []
for i in df_esg_clarity.itertuples():
    date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

df_esg_clarity['Date'] = date
df_esg_clarity['Source'] = 'ESG Clarity'

# df_esg_clarity = df_esg_clarity.loc[(df_esg_clarity['Date'] >= '2024-06-01')
#                      & (df_esg_clarity['Date'] <= '2024-12-31')]
df_esg_clarity

# soup