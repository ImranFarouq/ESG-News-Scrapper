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