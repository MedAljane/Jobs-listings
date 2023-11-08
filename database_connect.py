
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")


db = client["job_listings"]

collection = db["jobs"]

def insert_mongo (key,value):
    data = {key: value}
    collection.insert_one(data)

def find_mongo (link):
    result = collection.find({"Link": link})
    return result


