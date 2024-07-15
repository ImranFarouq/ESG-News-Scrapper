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
        
    news = []

    for i in range(1,6):
        try:
            url = f'https://www.gtreview.com/news/page/{i}/'

            # print(url)

            response = requests.get(url)

            soup = BeautifulSoup(response.content, 'html.parser')


            main = soup.find('div', class_='col-md-8')

            titles = main.find_all('article')
            # print(titles)

            for title in titles:
                
                heading = title.find('div' ,'content').h3.text.strip()
                image_link = title.find('figure', 'faded').a.img['src']

                try:
                    date = title.find('p', 'listdate').text.strip().split('/')[1].strip()
                except:
                    date = ''
                try:
                    description = title.find('div', 'content').text.strip().split('\n')[2].strip()
                except:
                    description = ''

                news.append([heading,  description, date,  title.h3.a['href'], image_link])
                # news.append([title.text.strip(), url + title.a['href']])

        except Exception as e:
            print(e)
            pass

    # # titles
    df = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])
    df['Source']= 'GTR View'

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


    print('Success')
    
except Exception as e:
    print('Error:', str(e))