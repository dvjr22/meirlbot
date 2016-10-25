############################################################
# file:    upvoteChecker.py                                #
# author:  Tyler Moon                                      #
# created: 10/11/2016                                      #
# purpose: This script checks the upvotes and tries to     #
# determine if the meme is trending up or trending down.   #
# If the meme is trending up then it starts the MemeCreator#
############################################################
import praw
from pymongo import MongoClient

EXITVALUE = 10

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
rposts = db.redditposts

# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='tmoonisthebest')


# Process all the submissions
#for submission in submissions:
for current in rposts.find():
    submission = r.get_submission(submission_id=current['redditId'])
    oldUpvotes = current['upvotes'] # Upvotes of the saved state in the database
    newUpvotes = submission.ups     # Upvotes of the current post
    print "Current Upvotes %s for id %s" % (newUpvotes,current['redditId'])
    if newUpvotes > oldUpvotes + EXITVALUE:
        print "Updating Value for id %s" % current['redditId']
        updatePost = {
            'upvoteTrend': current['upvoteTrend'] + 1
            }
        rposts.update_one({"_id": current["_id"]}, {"$set": updatePost})
    elif newUpvotes < oldUpvotes - EXITVALUE:
        print "Downgrading Value for id %s" % current['redditId']
        value = current['upvoteTrend']
        if value > 0:
            value = 0
        updatePost = {
            'upvoteTrend': value - 1
            }
        rposts.update_one({"_id": current["_id"]}, {"$set": updatePost})
