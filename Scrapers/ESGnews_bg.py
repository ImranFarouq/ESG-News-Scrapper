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

try:
    # from pymongo import MongoClient

    # # Create a connection to the MongoDB server
    # client = MongoClient("mongodb+srv://admin:imran123@cluster0.mz7q55x.mongodb.net/")

    # # Connect to a specific database (will create if it doesn't exist)
    # db = client['ESG_News']
        
    url = 'https://esgnews.bg/en/home-english/'

    news= []

    driver.get(url)
    time.sleep(10)
    scroll_to_bottom()

    driver.find_element(By.XPATH, '//a[@data-load="Load More"]').click()
    time.sleep(3)
    # driver.find_element(By.CLASS_NAME, 'button').click()
    # time.sleep(5)

    response = driver.page_source
    # find_element(By.CLASS_NAME, 'site-main')

    # div_blok
    soup = BeautifulSoup(response, 'html.parser')


    # titles = soup.find_all('div', 'jeg_postblock_content')
    titles = soup.find_all('article', 'jeg_post')

    # print(titles)
    for title in titles:
        # print(title)
        try:
            image_link = title.find('div', 'thumbnail-container').img['src']
            heading = title.find('h3', 'jeg_post_title').text.strip()
            date = title.find('div', 'jeg_meta_date').text.strip()
            description = title.find('div', 'jeg_post_excerpt').text.strip()
            link =  title.find('h3', 'jeg_post_title').a['href']

            # link = title.a['href']

            news.append([heading, description, date, link, image_link])
        except Exception as e:
            print(e)
            pass


    df_esg_news_bg = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])
    date = []
    for i in df_esg_news_bg.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df_esg_news_bg['Date'] = date
    df_esg_news_bg['Souce'] = 'ESGnews.bg'

    # df_esg_news_bg = df_esg_news_bg.loc[(df_esg_news_bg['Date'] >= '2024-06-01')
    #                      & (df_esg_news_bg['Date'] <= '2024-12-31')]

    df_esg_news_bg
    
    from sqlalchemy import create_engine

    import pymysql
    # URL-encoded password
    encoded_password = 'test%40123'
    
    # Create an engine to connect to the MySQL database using PyMySQL
    engine = create_engine(f'mysql+pymysql://test:{encoded_password}@13.201.128.161:3306/mysql')

    table_name = 'esg_news'
    df_esg_news_bg.to_sql(table_name, engine, if_exists='append', index=False)

    print("DataFrame saved to MySQL database successfully.")

    print('Success')
    
except Exception as e:
    print('Error:', str(e))