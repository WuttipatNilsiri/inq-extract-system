from pymongo import MongoClient
from bson.objectid import ObjectId

import bot

client = MongoClient()
print(str(client))


db = client.inq_extracting_database

collection = db["Main"]

def search(q):
        doc = collection.find_one(q)
        return doc

def searchbyID(_id):
        doc = collection.find_one({"_id": ObjectId(_id)})
        return doc

def save(data):
        _id = collection.insert_one(data).inserted_id
        print("save successful " + str(_id))
        return str(_id)

def update(_id,data):
        newvalues = { "$set": data }
        collection.update( { '_id': ObjectId(_id) }, newvalues )
        doc = searchbyID(_id)
        print(doc['Sender'])
        bot.send_update_mail(doc)


# print(searchbyID('delay',"5d258c54fc26df9718457839"))





# db = client.test_database
# print(db)


# post = {"author": "Mike",
#          "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"]}
# posts = db.posts

# post_id = posts.insert_one(post).inserted_id
# print(post_id)