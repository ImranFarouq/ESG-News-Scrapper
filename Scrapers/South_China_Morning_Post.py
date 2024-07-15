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
        
    url = 'https://www.scmp.com/topics/esg-investing'


    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')


    news = []

    url = 'https://www.scmp.com'

    titles = soup.find_all('div', class_='eplnudt2 css-t1fovn e1whfq0b0')
    # print(titles)

    for title in titles:
        try:
            # print(title)
            image_link = title.find('div', 'css-y5aea1 e1whfq0b5').a.figure.picture.img['src']
            heading = title.find('a', class_='e1whfq0b2 css-8ug9pk ef1hf1w0').text.strip()
            description = title.find('div', 'css-rofdc8 e1whfq0b4').text.strip() #.split('\n')[-1].strip()
            link = title.find('a', class_='e1whfq0b2 css-8ug9pk ef1hf1w0')['href']
            link = url + link
            date = title.find('div', 'css-16gl5nu e19yc7924').time.text.strip()

            news.append([heading, description,date,  link, image_link])
        except Exception as e:
            print(e)
            pass

    df_scmp = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    date = []
    for i in df_scmp.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df_scmp['Date'] = date
    df_scmp['Source'] = 'South China Morning Post'

    # df_scmp = df_scmp.loc[(df_scmp['Date'] >= '2024-06-01')
    #                      & (df_scmp['Date'] <= '2024-12-31')]
    df_scmp
    
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
    for row in df_scmp.itertuples():
        insert_query = f'''
            INSERT INTO esg_news (Title, Description, Date, Link, Image_URL)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (row.Title, row.Description, row.Date, row.Link, row.Image_URL))

    # Commit changes and close connection
    db.commit()
    db.close()
    print("DataFrame saved to MySQL database successfully.")

    print('Success')
    
except Exception as e:
    print('Error:', str(e))