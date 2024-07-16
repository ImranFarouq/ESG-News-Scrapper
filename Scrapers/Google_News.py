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

from newspaper import Article
from newspaper import Config
# from langdetect import detect
from datetime import datetime, timedelta, date

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start with maximized window

# Initialize the Chrome driver``
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


def headlines(link):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    link.strip()
    page = Article(str(link), config=config)
    try:
        page.download()
        page.parse()
        return page.title
    except:
        return 'Untitled Page'


def google_news_scraper():
    
    # ll = []
    y = []
    keywords = ['esg news today',
                'sustainability news',
                'esg global news',
                'esg news global',
                'environmental social and governance',
                'esg sustainability'
                ]
    for keyword in keywords:
        link = f'https://www.google.co.in/search?q={keyword}+news&sca_esv=64568e91d4c772e8&tbm=nws'
            

        data = []
        visited_urls = set()
        visited_url_date=set()
        # for link in ll:  
        driver.get(link)
        # driver.implicitly_wait(5)
        time.sleep(10)
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")

        news = soup.find_all("div",attrs={'class':"SoaBEf"})
        for row in news:
            des = {}
            
            title = row.find('div',attrs={'class':"n0jPhd ynAwRc MBeuO nDgy9d"}).text
            url = row.find("a",attrs={'class':"WlydOe"}).get('href')
            description = row.find('div',attrs={'class': 'GI74Re nDgy9d'}).text
            
            source = row.find('div',attrs={'class':"MgUUmf NUnG9d"}).text
            date = row.find('div',attrs={'class':"OSrXXb rbYSKb LfVVr"}).text
            
            images = row.find('img').get('src')
            
            # if url not in visited_urls and date not in visited_url_date:
            des['source'] = source
            des['link'] = url
            des['title'] = title
            des['date'] = date
            des['image'] = images
            des['description'] = description
            data.append(des)
            # visited_urls.add(url)

        today = datetime.today()
        # yesterday = today - timedelta(days=1)
        # yesterday = yesterday.strftime('%Y-%m-%d')
        

        DATE = []  
        for i in data:
            if i['date']:
                date = dateparser.parse(i['date'])
            if date:
                date = date.strftime("%Y-%m-%d")
                DATE.append(date)

            # article_date = dateparser.parse(article['date'])
            # if article_date and article_date.date() == (datetime.now() - timedelta(days=1)).date():
            #     filtered_data_final.append(article)

        filtered_data = []
        for data1, modified_date in zip(data, DATE):
            if modified_date:
                data1['Modified Dates'] = modified_date
                filtered_data.append(data1)

        filtered_data_final = []
        for data2 in filtered_data:
            if data2['Modified Dates']:
                modified_date = dateparser.parse(data2['Modified Dates'], date_formats=['%Y-%m-%d'])
                modified_date = modified_date.strftime('%Y-%m-%d')
                # if modified_date >= yesterday:
                filtered_data_final.append(data2)
                
        list1 = []
        for item in filtered_data_final:
            # title = item['title']
            # if detect(title) == 'en':  
            list1.append(item)  

        # for item in list1:
        #     item['title'] = headlines(item['link']) 

        list1 = [x for x in list1 if isinstance(x, dict) and x.get('title') is not None and ('Error' not in x['title']) and ('Captcha' not in x['title']) and
                ('Are you a robot?' not in x['title']) and ('Untitled Page' not in x['title']) and 
                ('Subscribe' not in x['title']) and ('You are being redirected...' not in x['title']) and 
                ('Not Acceptable!' not in x['title']) and ('403 Forbidden' not in x['title']) and 
                ('ERROR: The request could not be satisfied' not in x['title']) and ('Just a moment...' not in x['title']) and 
                ('403 - Forbidden: Access is denied.' not in x['title']) and ('Not Found' not in x['title']) and 
                ('Page Not Found' not in x['title']) and ('StackPath' not in x['title']) and ('Access denied' not in x['title'])
                and ('Yahoo' not in x['title']) and ('Stock Market Insights' not in x['title']) and 
                ('Attention Required!' not in x['title']) and ('Access Denied' not in x['title'])
                and ('403 forbidden' not in x['title']) and ('Too Many Requests' not in x['title'])
                and ('403 - Forbidden' not in x['title']) and ('NCSC' not in x['title'])
                and ('BC Gov News' not in x['title']) and ('The Verge' not in x['title']) and ('Trackinsight' not in x['title'])
                and ('Morning Headlines' not in x['title']) and ('Forbidden' not in x['title'])
                and ('forbidden' not in x['title']) and ('Detroit Free Press' not in x['title'])
                and ('reuters.com' not in x['title']) and ('403 unauthorized' not in x['title'])
                and ('403 not available now' not in x['title']) and ('Not Acceptable' not in x['title']) 
                and ('Your access to this site has been limited by the site owner' not in x['title'])
                and ('404 - File or directory not found.' not in x['title'])]

        for item in list1:
            if 'Fortune India: Business News, Strategy, Finance and Corporate ...' in item['source']:
                item['source'] = 'Fortune India'

        y.extend(list1)

    return pd.DataFrame(y)

try:
        
    news = google_news_scraper()
    news

    df = news.rename(columns={'title':'Title',
                    'source':'Source',
                    'Modified Dates':'Date',
                    'description':'Description',
                    'link':'Link',
                    'image': 'Image_URL'
                    })

    df = df[['Title', 'Description', 'Date', 'Link','Image_URL', 'Source']]

    print(df.shape)
    df = df.drop_duplicates(subset='Link')

    print('-'*15)
    print(df.shape)

    # Sort by today's date
    from datetime import datetime

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Get today's date as a datetime object
    today = pd.to_datetime(datetime.today().date())

    # today = datetime.today().date()
    df['Date_Diff'] = (df['Date'] - today).abs()

    # Sort the DataFrame by 'Date_Diff'
    sorted_df = df.sort_values(by='Date_Diff')

    # Drop the 'Date_Diff' column as it's no longer needed
    sorted_df = sorted_df.drop(columns=['Date_Diff'])
    # sorted_df

    date = []
    for i in sorted_df.itertuples():
        date.append(dateparser.parse(str(i[3])).strftime("%Y-%m-%d"))

    sorted_df['Date'] = date

    # print(sorted_df['Title'].sample(15))

    sorted_df.to_excel('Esg news.xlsx', index=False)


    import MySQLdb

    db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
    cursor = db.cursor()

    # # Fetch existing data
    # query = 'SELECT * FROM esg_news'
    # existing_df = pd.read_sql(query, db)

    # # Combine new data with existing data
    # combined_df = pd.concat([existing_df, sorted_df], ignore_index=True)

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
    for row in sorted_df.itertuples():
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
    
except Exception as e:
    print('Error:', str(e))