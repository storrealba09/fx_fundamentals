import csv, datetime
from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient('localhost' ,27017)
db = client.econ_db
m_data = db.econ_data
def save_csv(m_data):
    with open('econ_data_may2021.csv') as f:
      reader = csv.reader(f)
      for row in reader:
        a={}
        a['Country']= row[0].upper()
        if a['Country'] == 'USA':
            a['Country']= 'UNITED-STATES'
        if a['Country'] == 'UNITED KINGDOM':
            a['Country']= 'UNITED-KINGDOM'
        if a['Country'] == 'EURO AREA':
            a['Country']= 'EURO-AREA'
            
        if a['Country'] == 'NEW ZEALAND':
            a['Country']= 'NEW-ZEALAND'
            
        a['Code']= row[1]
        a['Continent']= row[2]
        a['Date']= datetime.datetime.strptime(row[4]+'-'+row[3], '%m-%Y')
        a['GDP']= row[5]
        a['CC']= row[6]
        a['PMI']= row[7]
        a['Inflation']= row[8]
        a['Interest Rate']= row[9]
        a['Currency (USD)']= row[10]
        a['Unemployment']= row[11]
        a['Stock Market']= row[12]
        if a['Date'] <= datetime.datetime.today():
            m_data.insert_one(a)
        

#save_csv(m_data)

def get_econ(country):
    x = m_data.find({'Country': country}).sort('Date', -1) #.sort({'date': -1})
    x = list(x)
    df = pd.DataFrame(x)
    #print(country)
    df.set_index('Date', inplace=True)
    
    df = df.replace(r'^\s*$', np.NaN, regex=True)
    #print(df)
    #sm = df[field].dropna()
    return (df[:20])

    #df['date'] = df['date'].astype(float)
    #df['date'] = pd.to_datetime(df['date'],unit='s')
    
    
#save_csv(m_data)
    #break
