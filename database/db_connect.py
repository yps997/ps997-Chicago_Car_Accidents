from pymongo import MongoClient

#connection
client = MongoClient('mongodb://localhost:27017/')

#data base
db = client['chicago_accidents']


#collections
accidents_collection = db['accidents']
locations_collection = db['locations']

