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
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")  # Start with maximized window
    chrome_options.add_argument("--headless")

    # Initialize the Chrome driver``
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    news= []

    for i in range(1,3):
        driver.get(f'https://www.esgtoday.com/category/esg-news/page/{i}/')
        
        time.sleep(10)
        
        response = driver.page_source
        # find_element(By.CLASS_NAME, 'site-main')

        # div_blok
        soup = BeautifulSoup(response, 'html.parser')
        # soup

        div = soup.find('main', 'tf_clearfix')

        titles = div.find_all('article', 'tf_clearfix')
        # titles = div.find_all('div', 'post-content')



        for title in titles:
            # print(title)
            try:
                image_link = title.find('figure', 'post-image').a.img['src']
                # print(image_link)
                heading = title.find('h2', 'post-title entry-title').text.strip()
                description = title.find('div', 'entry-content').text.strip()
                date = title.find('time', 'post-date entry-date updated').text.strip()
                link = title.h2.a['href']

                news.append([heading, description, date, link, image_link])
            except Exception as e:
                print(e)

    df_esg_tdy = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    date = []

    for i in df_esg_tdy.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df_esg_tdy['Date'] = date
    df_esg_tdy['Source'] = 'ESG Today'

    df_esg_tdy
    
    from sqlalchemy import create_engine

    import MySQLdb

    db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
    cursor = db.cursor()

   # Fetch existing data
    # query = 'SELECT * FROM esg_news'
    # existing_df = pd.read_sql(query, db)

    # # Combine new data with existing data
    # combined_df = pd.concat([existing_df, df_esg_tdy], ignore_index=True)

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
    for row in df_esg_tdy.itertuples():
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

    print('Source: ESg Today')
    
    today = datetime.now().strftime('%d-%b-%y,%I:%M %p')
    print(today)
    
    
except Exception as e:
    print('Error:', str(e))