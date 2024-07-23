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
    
    import time

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")  # Start with maximized window
    chrome_options.add_argument("--headless")

    # Initialize the Chrome driver``
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)


    url = 'https://www.3blmedia.com/news/all'  # Replace with the actual URL

    options = ['Environment', 'Green Infrastructure', 'Sustainable Development Goals', 'Sustainable Finance & Socially Responsible Investment']

    news = []

    for option in options:

        driver.get(url)
        
        # Locate the dropdown element
        dropdown_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'edit-field-fmr-primary-category-target-id')))
        
        # Create a Select object
        select = Select(dropdown_element)

        print('Scaraping data for ' + option)
        
        # Select the option 
        select.select_by_visible_text(option)
        
        wait = WebDriverWait(driver, 10)

        for i in range(1,3):
            
            time.sleep(5)
            
            response = driver.page_source
        
            soup = BeautifulSoup(response, 'html.parser')
        
            titles = soup.find_all('section', class_='teaser-newsfeed')
            # titles = soup.find_all('div', class_='col-md-9')

            urll = 'https://www.3blmedia.com'

            for title in titles:
                try:
                    # print(title)
                    heading = title.find('h4', class_='h5 teaser-title').text.strip()
                    description = title.text.strip().split('\n')[-1].strip()
                    date = title.find('p', class_='date').text.strip()

                    link = title.find('h4', class_='h5 teaser-title').span.a['href'] 
                    link = urll + link

                    image_link = title.find('div', class_='teaser-image').a.img['src']
                    image_link = urll + image_link

                    news.append([heading, description, date, link, image_link])
                except:
                    pass
            
            next_page_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.page-link[rel="next"]')))
            scroll_to_bottom()
            next_page_btn.click()

    df_3blmedia = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    date = []
    for i in df_3blmedia.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df_3blmedia['Date'] = date

    df_3blmedia['Source'] = '3BL Media'

    # df_3blmedia = df_3blmedia.loc[(df_3blmedia['Date'] >= '2024-06-01')
    #                     & (df_3blmedia['Date'] <= '2025-12-31')]

    df_3blmedia 
    
    from sqlalchemy import create_engine

    import MySQLdb

    db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
    cursor = db.cursor()

    # # Fetch existing data
    # query = 'SELECT * FROM esg_news'
    # existing_df = pd.read_sql(query, db)

    # # Combine new data with existing data
    # combined_df = pd.concat([existing_df, df_3blmedia], ignore_index=True)

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
    for row in df_3blmedia.itertuples():
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
    print('Source: 3BL Media')
    today = datetime.now().strftime('%d-%b-%y,%I:%M %p')
    print(today)
    
except Exception as e:
    print('Error:', str(e))