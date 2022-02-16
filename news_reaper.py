#init mongodb
from pymongo import MongoClient
client = MongoClient('localhost' ,27017)
db = client.news_db
data = db.news_data

with open('categories.txt') as f:
    lines = [line.rstrip() for line in f]

for x in data.find({},{ "_id": 1, "text": 1, "country": 1, "category":1 , "title":1, "date":1}):
    if x['category'] not in lines:
        a = data.delete_one({'_id': x['_id']})
        print(a)
