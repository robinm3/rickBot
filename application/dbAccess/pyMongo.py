import pymongo
from pymongo import MongoClient

uri = "mongodb://heroku_l3gldrl4:jmt44ea6t3a6p44t2c3aka23nj@ds157735.mlab.com:57735/heroku_l3gldrl4"
client = MongoClient(uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     retryWrites=False)

db = client.get_default_database()
collection = db["messenger"]


def getInDB(senderId, key):
    dataForKey = ""
    try:
        for dictionary in collection.find({"_id": senderId}):
            if key in dictionary:
                dataForKey = dictionary.get(key)
    except KeyError:
        dataForKey = ""
    return dataForKey


def setInDB(senderId, dictionary):
    post = {"_id": senderId}
    for key in dictionary:
        if collection.find_one({"_id": senderId}):
            collection.update_one(post, {"$set": {key: dictionary.get(key)}})
        else:
            post.update(dictionary)
            collection.insert_one(post)


def findInDB(senderId):
    found = False
    if collection.find_one({"_id": senderId}):
        found = True
    return found


def findAllInDB(key, value):
    found = list(collection.find({str(key): str(value)}))
    return found


def deleteFromDB(senderId):
    if findInDB(senderId):
        collection.delete_one({"_id": senderId})
