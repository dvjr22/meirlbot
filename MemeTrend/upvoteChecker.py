############################################################
# file:    upvoteChecker.py                                #
# author:  Tyler Moon                                      #
# created: 10/11/2016                                      #
# purpose: This script checks the upvotes and tries to     #
# determine if the meme is trending up or trending down.   #
# If the meme is trending up then it starts the MemeCreator#
############################################################
import praw
import time
import Queue
import threading
import urllib2
import os
from time import gmtime, strftime
from pymongo import MongoClient

EXITVALUE = 0

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
rposts = db.upvoteposts
r2posts = db.redditposts

# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='tmoonisthebest')

def alreadyExists(newID):
    return bool(db.mycollection.find_one({'redditId': newID}))

def getCurrentTime():
    return strftime("%Y-%m-%d %I:%m:%S")
def checkExit(sub,current):
    if((current['upvoteTrend'] > 2) and (sub.ups > 5)):
        return True
    else:
        return False

def checkDatabase():
    # Process all the submissions
    #for submission in submissions:
    for current in rposts.find():
        sub = r.get_submission(submission_id=current['redditId'])
        if checkExit(sub,current):
            print 'Found a meme and inserting it into the redditposts collection %s' % sub.url
            insertPost = {
                'url': sub.url,
                'upvotes': sub.ups,
                'redditId': sub.id,
                'localFile': ' ',
                'captionText': ' ',
                'updateFlag': False,
                'createdMemeFlag': False,
                'upvoteTrend': 1
            }
            r2posts.update_one({'redditId': sub.id},{"$set": insertPost},True)
            print 'Inserted document into redditposts'
            rposts.delete_one({'redditId':sub.id})
            print 'Removed document from upvoteposts'
        elif current['upvoteTrend'] < -5:
            print "Deleting document due to low upvoteTrend"
            rposts.delete_one({"_id":current["_id"]})
        else:
            submission = r.get_submission(submission_id=current['redditId'])
            oldUpvotes = current['upvote'] # Upvotes of the saved state in the database
            newUpvotes = submission.ups     # Upvotes of the current post
            print "Current Upvotes %s for id %s" % (newUpvotes,current['redditId'])

            if newUpvotes > oldUpvotes + EXITVALUE:
                print "Updating Value for id %s" % current['redditId']
                updatePost = {
                    'upvoteTrend': current['upvoteTrend'] + 1,
                    'upvote': newUpvotes,
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

def loadFromReddit():
    submissions = r.get_subreddit("me_irl").get_new(limit=100)
    for sub in submissions:
        if not alreadyExists(sub.id):
            upvoteTrend = 0
            if upvoteTrend > 0:
                upvoteTrend = upvoteTrend + 1
            else:
                upvoteTrend = 0

            redditId = sub.id
            url = sub.url
            upvotes = sub.ups
            print "Setting database document for %s, %s, %s, %s" % (upvotes, upvoteTrend, redditId, url)
            updatePost = {
                'upvoteTrend': upvoteTrend,
                'upvote': upvotes,
                'redditId': redditId,
                'url': url,
                'lastUpdate': getCurrentTime()
            }
            rposts.update_one({'redditId': redditId}, {"$set": updatePost},True) # The true argument here inserts a new document if an exisiting one isnt found
        else:
            print 'Post already in database'

def moveToMemeCreator():
    bool(db.mycollection.find_one({'upvoteTrend': {"$gt": 2}}))

def main():
    q = Queue.Queue()
    while not exitapp:
        print 'Starting up...'
        t1 = threading.Thread(target=loadFromReddit)
        t1.dameon = True
        t1.start()
        t2 = threading.Thread(target=checkDatabase)
        t2.dameon = True
        t2.start()
        print 'Waiting...'
        time.sleep(300)

def mainTesting():
    loadFromReddit()
    checkDatabase()

exitapp = False
if __name__ == '__main__':
    try:
        main()
        #mainTesting()
    except KeyboardInterrupt:
        exitapp = True
        os.abort()
