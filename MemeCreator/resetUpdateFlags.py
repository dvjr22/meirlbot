from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['meirlbot_mongodb']
rpost = db.redditposts
for current in rpost.find():
    updatePost = {
                    'updateFlag': False,
                 }
    rpost.update_one({"redditId": current['redditId']}, { "$set" : updatePost})
