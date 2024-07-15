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

try:
    # from pymongo import MongoClient

    # # Create a connection to the MongoDB server
    # client = MongoClient("mongodb+srv://admin:imran123@cluster0.mz7q55x.mongodb.net/")

    # # Connect to a specific database (will create if it doesn't exist)
    # db = client['ESG_News']

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

    from sqlalchemy import create_engine

    import pymysql
    # URL-encoded password
    encoded_password = 'test%40123'
    
    # Create an engine to connect to the MySQL database using PyMySQL
    engine = create_engine(f'mysql+pymysql://test:{encoded_password}@13.201.128.161:3306/mysql')

    table_name = 'esg_news'
    df_esg_clarity.to_sql(table_name, engine, if_exists='append', index=False)

    print("DataFrame saved to MySQL database successfully.")

    print('Success')
    # soup

except Exception as e:
    print('Error:', str(e))