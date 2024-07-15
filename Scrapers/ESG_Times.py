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

    url = 'https://www.esgtimes.in/category/esg/'
    news = []

    for i in range(1,3):
        response = requests.get(url + f'page/{i}/')

        soup = BeautifulSoup(response.content, 'html.parser')

        titles = soup.find_all('div', class_='post-container')

        for title in titles:

            image_link = title.find('div', 'post-thumbnail').img['src']

            title = title.find('div', 'post-content-container')
            
            heading = title.find('a', 'post-title').text.strip()
            date = title.find('a', 'post-date').text.strip()
            description = title.find('div', 'post-content').text.strip()
            
            news.append([heading, description, date, title.a['href'], image_link])
            # news.append([title.text.strip(), url + title.a['href']])
        # # titles
    df = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    date = []
    for i in df.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df['Date'] = date
    df['Source'] = 'ESG Times'
    df
    
    from sqlalchemy import create_engine
    import MySQLdb

    db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
    cursor = db.cursor()

    # Create table if it does not exist
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS esg_news (
            Title VARCHAR(255),
            Description TEXT,
            Date DATE,
            Link VARCHAR(255),
            Image_URL VARCHAR(255)
        )
    '''
    cursor.execute(create_table_query)

    # Insert DataFrame records into MySQL table
    for row in df.itertuples():
        insert_query = f'''
            INSERT INTO esg_news (Title, Description, Date, Link, Image_URL)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (row.Title, row.Description, row.Date, row.Link, row.Image_URL))

    # Commit changes and close connection
    db.commit()
    db.close()


    print("DataFrame saved to MySQL database successfully.")

    # soup
    print('Success')
    
except Exception as e:
    print('Error:', str(e))