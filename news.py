#init mongodb
import pandas as pd
from pymongo import MongoClient
from matplotlib import pyplot as plt
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions as selexcept
from selenium.webdriver.support import expected_conditions as EC
import time, os
from timeread import parsertime

'''import nltk, csv
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from scraper import get_sentiment

sia = SentimentIntensityAnalyzer()'''


client = MongoClient('localhost' ,27017)
db = client.news_db
m_data = db.news_data

countries =[
'united-states',
'united-kingdom',
'japan',
'canada',
'euro-area',
'china',
'new-zealand',
'australia',
'switzerland',
'denmark',
'sweden',
'singapore'
]

def get_news(country, how):#build URLs
    x = m_data.find({'country': country}).sort('date', -1) #.sort({'date': -1})
    x = list(x)
    df = pd.DataFrame(x)
    
    #df['date'] = df['date'].astype(float)
    df['date'] = pd.to_datetime(df['date'],unit='s')
    #print(df)
    #df['date'] = pd.to_datetime(df['date']) # convert column to datetime object
    #df.set_index('Date', inplace=True)
    #a = pd.DataFrame(df['Sentiment'].values[::-1])
    #a = a.rolling(30, min_periods=30).mean()
    #print(df)
    #print(q)
    #df['SMA_30'] = pd.DataFrame(a.values[::-1])
    #df['SMA_30'] = pd.Series([round(val, 3) for val in df['SMA_30']], index = df.index)
    #print(df['SMA_100'])
    #k = df['SMA_30']
    #df.columns = x.keys()
    #for i in x:
    #    print(i)
    #plt.plot(k)
    #plt.show()
    return df[:how]

def insert_news(zeta):
    print('inserting..')
    with open('categories.txt') as f:
        lines = [line.rstrip() for line in f]
    data = m_data.find_one({'country': zeta['country'][0]})
    #print(data)
    #m_data.delete_one({'country': zeta['country'][0]})
    #data.pop('_id', None)
    zeta['date'].reverse()
    zeta['title'].reverse()
    zeta['category'].reverse()
    zeta['text'].reverse()
    '''print(zeta)
    
    for n in zeta['date']:
        data['date'].insert(0, n)
    
    for e in zeta['title']:
        data['title'].insert(0, e)
    
    for r in zeta['category']:
        data['category'].insert(0, r)
    
    for t in zeta['text']:
        data['text'].insert(0, t)
    for y in zeta['country']:
        data['country'].insert(0, y)

    #data = get_sentiment(data,sia)'''
    print(zeta['date'][0])
    for k in range(len(zeta['date'])):
        #print(k)
        tetha = {'title': zeta['category'][k], 'category': zeta['title'][k], 'text':zeta['text'][k], 'date': zeta['date'][k], 'country': zeta['country'][k] }
        print(tetha)
        try:
            if tetha['category'] in lines:
                m_data.insert_one(tetha)
        except Exception as err:
            print(f'Other error occurred: {err}')
        
        
    print('updated '+zeta['country'][0])



def news_updater(countries):
    chromedriver_path = r'C:\Users\Administrator\Documents\chromedriver\chromedriver.exe'
    timeout = 20
    while (True):
        try:
            for pais in countries:
                browser = webdriver.Chrome(executable_path=chromedriver_path)
                browser.get('https://tradingeconomics.com/'+pais+'/news')
                WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="stream"]')))
                body = browser.find_elements_by_xpath('//*[@id="stream"]')
                a = body[0].text.split('\n')
                z= {'title': [], 'category': [], 'text':[], 'date': [], 'country': [] }
                last = m_data.find({'country': pais})
                #print(last[30])
                last = list(last)
                last = last[0]['date']
                #print(last)
                browser.quit()
                for i in range(0,len(a),4):
                    z['title'].append(a[i])
                    z['category'].append(a[i+1])
                    z['text'].append(a[i+2])
                    z['date'].append(parsertime(a[i+3]))
                    z['country'].append(pais)
                c = 0
                #print(z)

                new = []
                for j in z['date']:
                    if j > last:
                        new.append(c)
                    c += 1
                zeta = {'title': [], 'category': [], 'text':[], 'date': [], 'country': [] }
                for p in new:
                    zeta['title'].append(z['title'][p])
                    zeta['category'].append(z['category'][p])
                    zeta['text'].append(z['text'][p])
                    zeta['date'].append(z['date'][p])
                    zeta['country'].append(z['country'][p])
                insert_news(zeta)
        except Exception as err:
            print(f'Other error occurred: {err}')
                
        time.sleep(4000)

#news_updater(countries)
#                x = m_data.find({'country': country. 'date': j})
