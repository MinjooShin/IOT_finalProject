from pymongo import MongoClient

client = MongoClient('localhost', 27017)  
db = client.system_info  
usage_collection = db.usage_data 

usage_collection.find({})