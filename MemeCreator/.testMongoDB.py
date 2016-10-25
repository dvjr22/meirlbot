from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['meirlbot_mongodb']
rposts = db.redditposts
current = rposts.find_one()
print(current['redditId'])
