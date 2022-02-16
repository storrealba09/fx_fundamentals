#init mongodb
from pymongo import MongoClient
client = MongoClient('localhost' ,27017)
db = client.news_db
old_data = db.news_
new_data = db.news_data

p = 0
f = 0


for x in old_data.find({},{ "_id": 0, "text": 1, "country": 1, "category":1 , "title":1, "date":1}):
  print('==========================================================')
  print(len(x['text']))
  print(x['country'][0])
  #print('==========================================================')
  #print(x['text'][240])
  lista = []
  unique = []
  for i in range(len(x['text'])):
    zeta = {'title': x['category'][i], 'category': x['title'][i], 'text':x['text'][i], 'date': x['date'][i], 'country': x['country'][i] }
    if zeta not in lista:
      lista.append(zeta)
      p += 1
      try:
        new_data.insert_one(zeta)
      except Exception as err:
            print(f'Other error occurred: {err}')
    #if zeta['category'] not in unique:
      #unique.append(zeta['category'])
  print(len(lista))
  #print(unique)
  #for k in lista:
   # f += 1
    #new_data.insert_one(k)




print(p)
print('==========================================================')
#print(f)



    
