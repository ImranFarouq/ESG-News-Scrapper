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

try:
    # from pymongo import MongoClient

    # # Create a connection to the MongoDB server
    # client = MongoClient("mongodb+srv://admin:imran123@cluster0.mz7q55x.mongodb.net/")

    # # Connect to a specific database (will create if it doesn't exist)
    # db = client['ESG_News']

    import time

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start with maximized window

    # Initialize the Chrome driver``
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)


    urls = ['https://esgnews.com/category/global-news/',
            'https://esgnews.com/category/esg-reporting/',
            'https://esgnews.com/category/environmental',
            'https://esgnews.com/category/climate/',
            'https://esgnews.com/category/energy/', 
            'https://esgnews.com/category/sustainable-finance/', 
            ]

    news= []

    for url in urls:

        driver.get(url)  

        # Wait for the popup to appear (Adjust the time as necessary)
        time.sleep(10)

        scroll_to_bottom()

        load_more_btn = driver.find_element(By.CLASS_NAME, 'ajax-load-more').click()
        time.sleep(3)

        scroll_to_bottom()

        response = driver.page_source

        soup = BeautifulSoup(response, 'html.parser')

        titles = soup.find_all('div', 'has-thumbnail')

        for title in titles:

            image_link = title.find('a' , 'tt-post-img custom-hover').img['src']

            title = title.find('div', 'tt-post-info')

            heading = title.find('a', 'tt-post-title c-h5').text.strip()
            description = title.find('div', 'simple-text').text.strip()
            date = title.find('span', 'tt-post-date').text.strip()
            link = title.find('a', 'tt-post-title c-h5')['href']

            news.append([heading, description, date, link, image_link])

    df = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    date = []
    for i in df.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df['Date'] = date
    df['Source'] = 'ESG News'

    df = df.drop_duplicates('Title')
    # df = df[df['Date'] < '2024-06-30']
    
    from sqlalchemy import create_engine

    import pymysql
    # URL-encoded password
    encoded_password = 'test%40123'
    
    # Create an engine to connect to the MySQL database using PyMySQL
    engine = create_engine(f'mysql+pymysql://test:{encoded_password}@13.201.128.161:3306/mysql')
    table_name = 'esg_news'
    df.to_sql(table_name, engine, if_exists='append', index=False)

    print("DataFrame saved to MySQL database successfully.")

    print('Success')
    
except Exception as e:
    print('Error:', str(e))