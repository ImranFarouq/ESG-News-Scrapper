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
    chrome_options.add_argument("--start-maximized")  # Start with maximized window

    # Initialize the Chrome driver``
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://www.bbc.com/news/topics/cnvwkvd5q11t'


    news= []

    driver.get(url)
    time.sleep(10)

    for i in range(0,3):
        time.sleep(4)

        response = driver.page_source

        soup = BeautifulSoup(response, 'html.parser')
    
        titles = soup.find_all('a', 'sc-2e6baa30-0 gILusN')

        url = 'https://www.bbc.com'

        for title in titles:
            try:
                image_link = title.div.img['src']
                heading = title.find('h2', 'sc-4fedabc7-3 bvDsJq').text.strip()
                description = title.find('p', 'sc-ae29827d-0 cNPpME').text.strip()
                date =  title.find('span', 'sc-4e537b1-1 dkFuVs').text.strip()
                link = title['href']
                link = url + link

                news.append([heading, description, date, link , image_link ])
            
            except Exception as e:
                # print(e)
                pass
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="pagination-next-button"]').click()
        except:
            try:
                driver.find_element(By.CLASS_NAME, 'close-button').click()
                driver.find_element(By.CSS_SELECTOR, 'button[data-testid="pagination-next-button"]').click()
            except Exception as e:
                print(e)
                pass

    df_bbc = pd.DataFrame(news, columns=['Title', 'Description', 'Date', 'Link', 'Image_URL'])

    date = []
    for i in df_bbc.itertuples():
        date.append(dateparser.parse(i[3]).strftime("%Y-%m-%d"))

    df_bbc['Date'] = date

    df_bbc['Source'] = 'BBC'

    df_bbc = df_bbc.loc[(df_bbc['Date'] >= '2024-06-01')
                        & (df_bbc['Date'] <= '2024-12-31')]

    df_bbc
    print('Success')
except Exception as e:
    print('Error:', str(e))