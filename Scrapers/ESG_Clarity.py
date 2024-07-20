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

    import MySQLdb

    db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
    cursor = db.cursor()

    # # Fetch existing data
    # query = 'SELECT * FROM esg_news'
    # existing_df = pd.read_sql(query, db)

    # # Combine new data with existing data
    # combined_df = pd.concat([existing_df, df_esg_clarity], ignore_index=True)

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
    for row in df_esg_clarity.itertuples():
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
    # soup
    from datetime import datetime

    print('Source: ESG Clarity')
    
    today = datetime.now().strftime('%d-%b-%y,%I:%M %p')
    print(today)
    

except Exception as e:
    print('Error:', str(e))