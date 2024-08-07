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

    import time

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")  # Start with maximized window
    chrome_options.add_argument("--headless")

    # Initialize the Chrome driver``
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the target URL
    driver.get('https://www.sustainabilitymenews.com/environmental-social')  # Replace with the actual URL

    # Wait for the popup to appear (Adjust the time as necessary)
    time.sleep(10)


    def scroll_to_bottom():
        actions = ActionChains(driver)

        # Number of times to send the "End" key
        number_of_times = 3

        # Send the "End" key multiple times
        for _ in range(number_of_times):
            actions.send_keys(Keys.END).perform()

            # Adding a small delay to allow the page to load
            time.sleep(1)

    scroll_to_bottom()


    load_more_btn = driver.find_element(By.CLASS_NAME, 'load-more-m_button__1mmf1').click()
    time.sleep(3)

    scroll_to_bottom()

    response = driver.page_source
    # find_element(By.CLASS_NAME, 'site-main')


    soup = BeautifulSoup(response, 'html.parser')
    # soup

    # div_blok = soup.find('div' , 'full-width-with-padding')
    news = []

    # print(div_blok)

    # titles = soup.find_all('a', attrs={'aria-label': 'headline'})
    # titles = soup.find_all('div', class_='arr--story-content storycard-m_content__1Q9vq')

    titles = soup.find_all('div', class_='three-col-six-stories-m_card__Or020')


    # print(titles)

    # titles = div.find_all('h2', 'entry-title')

    for title in titles:
        image_link = title.find('div', 'hero-image-m_image-wrapper__2EIzt').figure.img['src']
        image_link = 'https:' + image_link

        try:
            heading = title.find('h2', class_='headline-m_headline__3_NhV headline-m_dark__en3hW').text.strip()
        except:
            heading = title.find('h5', class_='headline-m_headline__3_NhV headline-m_dark__en3hW').text.strip()

        date_time = title.find('div', class_='time arr--publish-time timestamp-m_time__2v46i timestamp-m_dark__2lk9E').text.strip()

        try:
            description = title.find('p', class_='p-alt arr--sub-headline arrow-component  subheadline-m_subheadline__3fd7z subheadline-m_dark__28u00').text.strip()
        except:
            description = ''

        link = title.find('a', attrs={'aria-label': 'headline'})['href']
        
        news.append([heading,  description, date_time, link, image_link])
        
    titles = soup.find_all('div', class_='one-col-story-list-m_one-col-border-default__2BDg7')

    for title in titles:
        image_link = title.find('div', 'hero-image-m_image-wrapper__2EIzt').figure.img['src']
        image_link = 'https:' + image_link

        # try:
        heading = title.find('h6', class_='headline-m_headline__3_NhV headline-m_dark__en3hW').text.strip()
        # except:
        #     heading = title.find('h5', class_='headline-m_headline__3_NhV headline-m_dark__en3hW').text.strip()

        date_time = title.find('div', class_='time arr--publish-time timestamp-m_time__2v46i timestamp-m_dark__2lk9E').text.strip()

        try:
            description = title.find('div', {'data-test-id': 'subheadline'}).text.strip()
        except:
            description = ''

        link = title.find('a', attrs={'aria-label': 'headline'})['href']
        
        news.append([heading,  description, date_time, link, image_link])
        
    df = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    date = []
    for i in df.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df['Date'] = date
    df['Source'] = 'Sustainability News'
    df
    
    from sqlalchemy import create_engine

    import MySQLdb

    db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
    cursor = db.cursor()

    # Fetch existing data
    # query = 'SELECT * FROM esg_news'
    # existing_df = pd.read_sql(query, db)

    # # Combine new data with existing data
    # combined_df = pd.concat([existing_df, df], ignore_index=True)

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
    for row in df.itertuples():
        insert_query = f'''
            INSERT INTO esg_news (Title, Description, Date, Link, Image_URL, Source)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (row.Title, row.Description, row.Date, row.Link, row.Image_URL, row.Source))

    # Commit changes and close connection
    db.commit()
    db.close()

    try:
        driver.close()
    except:
        pass

    print("DataFrame saved to MySQL database successfully.")

    print('Success')
    from datetime import datetime

    print('Source: Sustainability News')
    
    today = datetime.now().strftime('%d-%b-%y,%I:%M %p')
    print(today)
    
    
except Exception as e:
    print('Error:', str(e))