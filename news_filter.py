#init mongodb
from pymongo import MongoClient
client = MongoClient('localhost' ,27017)
db = client.news_db
data = db.news_data

lista = []

for x in data.find({},{ "_id": 1, "text": 1, "country": 1, "category":1 , "title":1, "date":1}):
    #print(x['category'])
    if x['category'] not in lista:
        lista.append(x['category'])

final = []

for p in lista:
    print(p)
    answer = input("Va o no va? : ") 
    if answer == "y": 
        final.append(p)
    elif answer == "n": 
        pass
    else: 
        print("Please enter yes or no.")
with open('categories.txt', 'w') as f:
    for q in final:
        f.write("%s\n" % q)
#print(lista)
    #break
