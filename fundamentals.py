from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_financial_report(country):#build URLs
    urlindicators = 'https://tradingeconomics.com/'+country+'/forecast'
    text_soup_financials = BeautifulSoup(requests.get(urlindicators).text,"html")
    titlesfinancials = text_soup_financials.findAll('tr')
    for a in titlesfinancials:
        if 'Markets' in a.text:
            index = [th.text for th in  a.findAll('th',{'class': 'table-value'}) if th.text]
            index[0] = 'Actual'
        if 'Currency' in a.text:
            currency = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                currency[i] = float(currency[i])
        if 'Stock Market' in a.text:
            stock = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                stock[i] = float(stock[i])
        if 'GDP Growth Rate' in a.text:
            gdp = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                gdp[i] = float(gdp[i])
        if 'Interest Rate' in a.text:
            interest = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                interest[i] = float(interest[i])
        
        #BONDS
        if 'Government Bond 10Y' in a.text:
            bonds = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                bonds[i] = float(bonds[i])
        if ((country == 'EURO-AREA') or (country == 'euro-area')):
            bonds = []
            for i in range(0,6):
                bonds.append('NA')

        if 'Unemployment Rate' in a.text:
            unemployment = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                unemployment[i] = float(unemployment[i])
        if 'Inflation Rate' in a.text:
            inflation = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                inflation[i] = float(inflation[i])
        if 'Consumer Confidence' in a.text:
            confidence = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                confidence[i] = float(confidence[i])
        if 'Manufacturing PMI' in a.text:
            manufacture = [td.text for td in  a.findAll('td',{'class': 'table-value'}) if td.text]
            for i in range(0,6):
                manufacture[i] = float(manufacture[i])
        if country == 'DENMARK':
            manufacture = []
            for i in range(0,6):
                manufacture.append('NA')
        if country == 'SINGAPORE':
            confidence = []
            for i in range(0,6):
                confidence.append('NA')


    fun_df= pd.DataFrame({'Currency': currency,'Stock Market': stock,'GDP Growth Rate':gdp,'Government Bond 10Y': bonds,'Unemployment Rate': unemployment,'Inflation Rate':
                  inflation,'Interest Rate': interest,'Manufacturing PMI': manufacture, 'Consumer Confidence':confidence},index=index)

    fun_df.reset_index(inplace=True)

    return fun_df
