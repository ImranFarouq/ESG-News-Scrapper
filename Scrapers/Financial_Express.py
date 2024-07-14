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
    from pymongo import MongoClient

    # Create a connection to the MongoDB server
    client = MongoClient("mongodb+srv://admin:imran123@cluster0.mz7q55x.mongodb.net/")

    # Connect to a specific database (will create if it doesn't exist)
    db = client['ESG_News']
        
    import time

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start with maximized window

    # Initialize the Chrome driver``
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://www.financialexpress.com/about/sustainability/'


    news= []

    driver.get(url)

    for i in range(1,5):
        time.sleep(10)

        response = driver.page_source
        
        soup = BeautifulSoup(response, 'html.parser')
        
        titles = soup.find_all('article', 'post-has-image')

        for title in titles:
            try:
                image_link = title.figure.a.img['src']
                
                heading = title.find('div', 'entry-title').text.strip()
                description = title.find('div', 'hide-for-small-only post-excerpt').text.strip()
                date =  title.find('div', 'entry-meta').text.strip()
                link = title.find('div', 'entry-title').a['href']

                news.append([heading, description, date, link, image_link])
            except Exception as e:
                # print(e)
                pass
        
        load_more_btn = driver.find_element(By.CSS_SELECTOR, 'a.next.page-numbers').click()

    df_financial_express = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    df_financial_express['Date'] = df_financial_express['Date'].str.replace('Updated:', '')


    date = []
    for i in df_financial_express.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df_financial_express['Date'] = date
    df_financial_express['Source'] = 'Financial Express'

    # df_financial_express = df_financial_express.loc[(df_financial_express['Date'] >= '2024-06-01')
    #                      & (df_financial_express['Date'] <= '2024-12-31')]

    df_financial_express
        # Convert DataFrame to dictionary
    data_dict = df_financial_express.to_dict("records")

    # Insert data into a MongoDB collection (will create if it doesn't exist)
    collection = db['News']
    collection.insert_many(data_dict)

    print("DataFrame saved to MongoDB successfully.")

    print('Success')
    
except Exception as e:
    print('Error:', str(e))