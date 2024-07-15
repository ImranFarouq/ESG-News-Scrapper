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


    news = []

    for i in range(1,20):
        url = f'https://www.businessgreen.com/type/news/page/{i}'


        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')


        titles = soup.find_all('div', class_='mb-2')

        url = 'https://www.businessgreen.com'

        for title in titles:
            try:
                heading = title.find('div', class_='platformheading').text.strip()
                description = title.find('div', 'searchpara').text.strip() #.split('\n')[-1].strip()
                
                link = title.find('div', 'platformheading').h4.a['href']
                link = url + link

                date = title.find('div', 'published').text.strip()
                # image_link = title.find('div', 'listing-left').div.a.img['src']
                image_link = title.div.div.div.a.img['src']


                news.append([heading, description, date, link, image_link])

            except Exception as e:
                # print(e)
                pass

    df_business_green = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    df_business_green['Date'] = df_business_green['Date'].apply(lambda i : i.split('\n')[0])

    date = []
    for i in df_business_green.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df_business_green['Date'] = date
    df_business_green['Source'] = 'Business Green'

    # df_business_green = df_business_green.loc[(df_business_green['Date'] >= '2024-06-01')
    #                      & (df_business_green['Date'] <= '2024-12-31')]

    df_business_green

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
    for row in df_business_green.itertuples():
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