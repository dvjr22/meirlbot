############################################################
# file:    upvoteChecker.py                                #
# author:  Tyler Moon                                      #
# created: 10/11/2016                                      #
# purpose: This script checks the upvotes and tries to     #
# determine if the meme is trending up or trending down.   #
# If the meme is trending up then it starts the MemeCreator#
############################################################
import praw # praw stands for "Python Reddit API Wrapper"
import time
import Queue
import threading
import urllib2
import os
import logging
import json
from logging.config import fileConfig
from time import gmtime, strftime
from pymongo import MongoClient
from pprint import pprint
from RabbitMQ.RabbitMQHandler import RabbitMQHandler

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
upvotepostsCollection = db.upvoteposts
redditpostsCollection = db.redditposts

# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='tmoonisthebest')

# Configure the RabbitMQ logger
logHandler = RabbitMQHandler(exchange='logs', routing_key='log', queueType='direct')

# Boolean for passing the KeyboardInterrupt signal onto the threads
exitapp = False

# Global variables
upvoteTrendExitCondition = 0
upvoteTrendNegativeCutoff = 0
upvoteExitCondition = 0
exitvalue = 0

# Load the json file for the config variables
try:
    logHandler.publishMsg('(upvoteChecker) Loading global variables from upvoteCheckerConfig.json')
    with open('upvoteCheckerConfig.json') as config_file:
        data = json.load(config_file)
        try:
            upvoteTrendExitCondition = data["upvoteTrendExitCondition"]
            logHandler.publishMsg('(upvoteChecker) Loaded %s for upvoteTrendExitCondition' % upvoteTrendExitCondition)
            upvoteTrendNegativeCutoff = data["upvoteTrendNegativeCutoff"]
            logHandler.publishMsg('(upvoteChecker) Loaded %s for upvoteTrendNegativeCutoff' % upvoteTrendExitCondition)
            upvoteExitCondition = data["upvoteExitCondition"]
            logHandler.publishMsg('(upvoteChecker) Loaded %s for upvoteExitCondition' % upvoteExitCondition)
            exitvalue = data["exitvalue"]
            logHandler.publishMsg('(upvoteChecker) Loaded %s for exitvalue' % exitvalue)
        except:
            logHandler.publishMsg('(upvoteChecker) Problem parsing variables from upvoteCheckerConfig.json')
except:
    logHandler.publishMsg('(upvoteChecker) Could not load upvoteCheckerConfig.json file!')
    raise

# Simple function for returning a formatted datetime stamp
def getCurrentTime():
    return strftime("%Y-%m-%d %I:%m:%S")

# Simple function that returns a boolean for if the exit condition of a meme is found
# A meme must have both the upvoteTrend greater than upvoteTrendExitCondition
# and also a current upvote total of greather than upvoteTrendNegativeCutoff
def checkExit(sub,current):
    if((current['upvoteTrend'] > upvoteTrendExitCondition) and (sub.ups > upvoteExitCondition)):
        return True
    else:
        return False

# The checkDatabase function loops through all the documents in the upvoteposts collection.
# If the document meets the exit conditions laid out in checkExit then the document
# is moved from the upvotepost colleciton to the redditposts collection for the
# MemeCreator Bot.
# If the documents upvoteTrend is lower than the global var upvoteTrendNegativeCutoff
# then the document is deleted
# If the documents upvoteTrend is greater than its current value plus the exitvalue
# then its value is incremented
# If the documents upvoteTrend is lower than its current value minus the exitvalue
# then its value is decremented
def checkDatabase():
    logHandler.publishMsg('(upvoteChecker) Checking database and updating submissions')
    # Process all the submissions in the upvoteposts collection
    for current in upvotepostsCollection.find():
        logHandler.publishMsg('(upvoteChecker) Checking database with id: %s' % current['_id'])
        # Get the post based off the redditId
        sub = r.get_submission(submission_id=current['redditId'])
        if checkExit(sub,current):
            # Found a meme due to the upvoteTrend and upvotes being above the threshold
            logHandler.publishMsg('(upvoteChecker) Found a meme and inserting it into the redditposts collection %s' % sub.url)
            # New document to insert
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
            # Upsert the document into the redditposts collection
            redditpostsCollection.update_one({'redditId': sub.id},{"$set": insertPost},True)
            logHandler.publishMsg('(upvoteChecker) Inserted document into redditposts')

            # Remove the document from the upvoteposts collection
            upvotepostsCollection.delete_one({'redditId':sub.id})
            logHandler.publishMsg('(upvoteChecker) Removed document from upvoteposts')

        elif current['upvoteTrend'] < upvoteTrendNegativeCutoff:
            # If the upvoteTrend gets below -5 then delete the document and stop tracking it
            logHandler.publishMsg('(upvoteChecker) Deleting document due to low upvoteTrend')
            upvotepostsCollection.delete_one({"_id":current["_id"]})
        else:
            oldUpvotes = current['upvote'] # Upvotes of the saved state in the database
            newUpvotes = sub.ups     # Upvotes of the current post
            logHandler.publishMsg('(upvoteChecker) Current Upvotes %s for id %s' % (newUpvotes,current['redditId']))

            # If the upvotes has increased by more than the exitvalue variable then increment the upvoteTrend
            if newUpvotes > oldUpvotes + exitvalue:
                logHandler.publishMsg('(upvoteChecker) Updating Value for id %s' % current['redditId'])
                updatePost = {
                    'upvoteTrend': current['upvoteTrend'] + 1,
                    'upvote': newUpvotes,
                    }
                logHandler.publishMsg('(upvoteChecker) Updating document with id %s' % current["_id"])
                upvotepostsCollection.update_one({"_id": current["_id"]}, {"$set": updatePost})
            # If the upvotes has decremented by more than the exitvalue variable then decrement the upvoteTrend
            elif newUpvotes < oldUpvotes - exitvalue:
                logHandler.publishMsg('(upvoteChecker) Downgrading Value for id %s' % current['redditId'])
                updatePost = {
                    'upvoteTrend': current['upvoteTrend'] - 1
                    }
                logHandler.publishMsg('(upvoteChecker) Updating document with id %s' % current["_id"])
                upvotepostsCollection.update_one({"_id": current["_id"]}, {"$set": updatePost})
# Simple function that returns a boolean of if the document with the redditId newID already exists in the collection or not
def alreadyExists(newID):
    exists = bool(db.mycollection.find_one({'redditId': newID}))
    logHandler.publishMsg('(upvoteChecker) Already exists check for %s is %s' % (newID,exists))
    return exists

# loadFromReddit is a function that loops through the top 100 posts on
# www.reddit.com/r/me_irl/new. As long as the submission is not already in the
# collection it adds to the collection upvoteposts
def loadFromReddit():
    submissions = r.get_subreddit("me_irl").get_new(limit=100)
    logHandler.publishMsg('(upvoteChecker) Loading submissions %s' % submissions)
    logHandler.publishMsg('(upvoteChecker) Loading in new data from reddit')
    for sub in submissions:
        if not alreadyExists(sub.id):
            upvoteTrend = 0
            redditId = sub.id
            url = sub.url
            upvotes = sub.ups
            logHandler.publishMsg('(upvoteChecker) Inserting database document for %s, %s, %s, %s' % (upvotes, upvoteTrend, redditId, url))
            updatePost = {
                'upvoteTrend': upvoteTrend,
                'upvote': upvotes,
                'redditId': redditId,
                'url': url,
                'lastUpdate': getCurrentTime()
            }
            upvotepostsCollection.update_one({'redditId': redditId}, {"$set": updatePost},True) # The true argument here inserts a new document if an exisiting one isnt found
        else:
            logHandler.publishMsg('(upvoteChecker) Submission %s already in database' % sub.id)

def main():
    logHandler.publishMsg('(upvoteChecker) Starting main process')
    q = Queue.Queue()
    while not exitapp:
        logHandler.publishMsg('(upvoteChecker) Starting loadFromReddit thread')
        loadFromRedditThread = threading.Thread(target=loadFromReddit)
        loadFromRedditThread.dameon = True
        loadFromRedditThread.start()
        logHandler.publishMsg('(upvoteChecker) Starting checkDatabase thread')
        checkDatabaseThread = threading.Thread(target=checkDatabase)
        checkDatabaseThread.dameon = True
        checkDatabaseThread.start()
        time.sleep(300)

def mainTesting():
    loadFromReddit()
    checkDatabase()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        os.abort()
