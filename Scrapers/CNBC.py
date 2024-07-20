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

    from sqlalchemy import create_engine

    import MySQLdb

    db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
    cursor = db.cursor()

    # # Fetch existing data
    # query = 'SELECT * FROM esg_news'
    # existing_df = pd.read_sql(query, db)

    # # Combine new data with existing data
    # combined_df = pd.concat([existing_df, df_cnbc], ignore_index=True)

    # # Drop duplicates
    # combined_df.drop_duplicates(subset=['Title', 'Description', 'Date', 'Link', 'Image_URL'], inplace=True)

    # Create table if it does not exist
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS esg_news (
            Title VARCHAR(255),
            Description TEXT,
            Date DATE,
            Link VARCHAR(255),
            Image_URL VARCHAR(255),
            Source VARCHAR(255)
        )
    '''
    cursor.execute(create_table_query)

    # Truncate the table to remove old data
    # cursor.execute('TRUNCATE TABLE esg_news')

    # Insert the cleaned DataFrame back into MySQL table
    for row in df_cnbc.itertuples():
        insert_query = f'''
            INSERT INTO esg_news (Title, Description, Date, Link, Image_URL, Source)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (row.Title, row.Description, row.Date, row.Link, row.Image_URL, row.Source))

    # Commit changes and close connection
    db.commit()
    db.close()

    print("DataFrame saved to MySQL database successfully.")

    print('Success')
    from datetime import datetime

    print('Source: CNBC')
    
    today = datetime.now().strftime('%d-%b-%y,%I:%M %p')
    print(today)
    
    
except Exception as e:
    print('Error:', str(e))