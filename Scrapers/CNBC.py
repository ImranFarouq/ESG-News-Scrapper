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


url = 'https://www.cnbc.com/climate/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

news = []

# div = soup.find('div', 'PageBuilder-col-9 PageBuilder-col')
titles = soup.find_all('div', class_='Card-rectangleToLeftSquareMedia')


for title in titles:
    heading = title.find('a', class_='Card-title').text.strip()
    date = title.find('span', class_='Card-time').text.strip()
    link = title.find('a', class_='Card-title')['href']
    image_link = title.div.a.div.div.picture.img['src']
    description = ''

    news.append([heading, description, date , link, image_link])


df_cnbc = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

date = []

for i in df_cnbc.itertuples():
    date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

df_cnbc['Date'] = date

df_cnbc['Source'] = 'CNBC'

# df_cnbc = df_cnbc.loc[(df_cnbc['Date'] >= '2024-06-01')
#                      & (df_cnbc['Date'] <= '2024-12-31')]

df_cnbc