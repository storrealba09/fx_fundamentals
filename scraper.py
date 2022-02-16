# Selenuim imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions as selexcept
from selenium.webdriver.support import expected_conditions as EC
import time, os

# Pandas imports using Pandas for structuring our data
import pandas as pd
from datetime import datetime
import os.path
import re
import sys
import glob
from timeread import parsertime
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv

# Time and date-time (mainly for using delays between clicks)
import time

#init mongodb
from pymongo import MongoClient
client = MongoClient('localhost' ,27017)
db = client.news_db
m_data = db.news_data

# Change this to your own chromedriver path!
chromedriver_path = r'C:\Users\Administrator\Documents\chromedriver\chromedriver.exe'


# This will open the Chrome window
#option = webdriver.ChromeOptions()
#option.add_argument(' — incognito')


def get_news(m_data, chromedriver_path, country):
    browser = webdriver.Chrome(executable_path=chromedriver_path)
    browser.get('https://tradingeconomics.com/'+country+'/news')

    # Wait 20 seconds for page to load
    timeout = 20
    b=[]
    a=[0]
    q = []
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="stream"]')))

        while ((browser.find_element_by_id('stream-btn')) and (b != a)):
            b = a
            browser.find_element_by_id('stream-btn').click()
            body = browser.find_elements_by_xpath('//*[@id="stream"]')
            a = body[0].text.split('\n')
            time.sleep(6)

        browser.quit()
        z= {'title': [], 'category': [], 'text':[], 'date': [], 'country': [] }

        for i in range(0,len(a),4):
            z= {'title': a[i], 'category': a[i+1], 'text': a[i+2], 'date': parsertime(a[i+3]), 'country': country }
            '''z['title'].append(a[i])
            z['category'].append(a[i+1])
            z['text'].append(a[i+2])
            z['date'].append(parsertime(a[i+3]))
            z['country'].append(country)'''
            m_data.insert_one(z)
            print(z)


        #print(f_label[0].text)
        #print(f_headline[0].text)
        #z = pd.DataFrame.from_dict(z)
        #print(z)
        return()
        #print(f_time[0].text)
        #browser.quit()
    except Exception as e:
        print(e)
        browser.quit()

countries =[
'united-states', 'china', 'canada', 'japan', 'united-kingdom','new-zealand',
'australia', 'singapore', 'europe', 'sweden', 'switzerland', 'denmark'
]
#initialize sentiment analysis
import nltk, csv
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()


def get_sentiment(data,sia):
    '''# # stock market lexicon
    stock_lex = pd.read_csv('stock_lex.csv')
    stock_lex['sentiment'] = (stock_lex['Aff_Score'] + stock_lex['Neg_Score'])/2
    stock_lex = dict(zip(stock_lex.Item, stock_lex.sentiment))
    stock_lex = {k:v for k,v in stock_lex.items() if len(k.split(' '))==1}
    stock_lex_scaled = {}
    for k, v in stock_lex.items():
        if v > 0:
            stock_lex_scaled[k] = v / max(stock_lex.values()) * 4
        else:
            stock_lex_scaled[k] = v / min(stock_lex.values()) * -4'''

    # # Loughran and McDonald
    positive = []
    with open('lm_positive.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
          positive.append(row[0].strip())

    negative = []
    with open('lm_negative.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
          entry = row[0].strip().split(" ")
          if len(entry) > 1:
              negative.extend(entry)
          else:
              negative.append(entry[0])

    final_lex = {}
    final_lex.update({word:2.0 for word in positive})
    final_lex.update({word:-2.0 for word in negative})
    #final_lex.update(stock_lex_scaled)
    final_lex.update(sia.lexicon)
    sia.lexicon = final_lex
    data['sentiment']= []
    for text in data['text']:
        sentiment = sia.polarity_scores(text)['compound']
        data['sentiment'].append(sentiment)
    return data


def scrap(countries):
    n = len(countries)
    c = 0
    for i in countries:
        c+= 1
        print('vamos por '+str(c)+'/'+str(n))
        print(i)
        get_news(m_data, chromedriver_path, i)
        #data = get_sentiment(data,sia)

#scrap(countries)


