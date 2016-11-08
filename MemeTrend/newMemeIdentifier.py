############################################################
# file:    newMemeIdentifier.py                            #
# author:  Tyler Moon                                      #
# created: 11/07/2016                                      #
# purpose: This script determines if a trending meme should#
# be moved to the redditposts collection to be processed   #
# into a meme by the MemeCreator Bot                       #
############################################################
# REVIEW: See if any of these imports are not being used
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
from RabbitMQ.RabbitMQHandler import RabbitMQLogger
from RabbitMQ.RabbitMQHandler import RabbitMQDatabase

# NOTE: After all database queries are changed to rabbitmq messages then delete this connection
# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
 = db.upvoteposts
redditpostsCollection = db.redditposts

# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='tmoonisthebest')

# Boolean for passing the KeyboardInterrupt signal onto the threads
exitapp = False

# Configure the RabbitMQ logger
logHandler = RabbitMQLogger()
upvotepostsHandler = RabbitMQDatabase(collectionName='upvoteposts')
#upvotepostsHandler = RabbitMQHandler(exchange='database', routing_key='upvotepostsupdate', queueType='direct')
#redditpostsHandler = RabbitMQHandler(exchange='database', routing_key='redditpostsupdate', queueType='direct')

# Simple function that returns a boolean for if the exit condition of a meme is found
# A meme must have both the upvoteTrend greater than upvoteTrendExitCondition
# and also a current upvote total of greather than upvoteTrendNegativeCutoff
def checkExit(sub,current):
    if((current['upvoteTrend'] > upvoteTrendExitCondition) and (sub.ups > upvoteExitCondition)):
        return True
    else:
        return False

# Global variables
upvoteTrendExitCondition = 0
upvoteTrendNegativeCutoff = 0
upvoteExitCondition = 0
exitvalue = 0

# Load the json file for the config variables
try:
    logHandler.logMessage('(newMemeIdentifier) Loading global variables from newMemeIdentifierConfig.json')
    with open('newMemeIdentifierConfig.json') as config_file:
        data = json.load(config_file)
        try:
            upvoteTrendExitCondition = data["upvoteTrendExitCondition"]
            logHandler.logMessage('(newMemeIdentifier) Loaded %s for upvoteTrendExitCondition' % upvoteTrendExitCondition)
            upvoteTrendNegativeCutoff = data["upvoteTrendNegativeCutoff"]
            logHandler.logMessage('(newMemeIdentifier) Loaded %s for upvoteTrendNegativeCutoff' % upvoteTrendExitCondition)
            upvoteExitCondition = data["upvoteExitCondition"]
            logHandler.logMessage('(newMemeIdentifier) Loaded %s for upvoteExitCondition' % upvoteExitCondition)
            exitvalue = data["exitvalue"]
            logHandler.logMessage('(newMemeIdentifier) Loaded %s for exitvalue' % exitvalue)
        except:
            logHandler.logMessage('(newMemeIdentifier) Problem parsing variables from newMemeIdentifierConfig.json')
except:
    logHandler.logMessage('(newMemeIdentifier) Could not load newMemeIdentifierConfig.json file!')
    raise

# TODO: Update this comment with the message stuff
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
    logHandler.logMessage('(newMemeIdentifier) Checking database and updating submissions')
    # Process all the submissions in the upvoteposts collection
    data = upvotepostsHandler.fetchData('{\"redditId\":\"595tr8\"}')
    logHandler.logMessage('  [x] (newMemeIdentifier) Received %s data' % data)
    jsonData = json.loads(data)
    for current in jsonData:
        logHandler.logMessage('(newMemeIdentifier) Checking database with id: %s' % current['redditId'])
        # Get the post based off the redditId
        sub = r.get_submission(submission_id=current['redditId'])
        if(sub,current):
            # Found a meme due to the upvoteTrend and upvotes being above the threshold
            logHandler.logMessage('(newMemeIdentifier) Found a meme and inserting it into the redditposts collection %s' % sub.url)
            # New document to insert
            #insertPost = '{\"url\": \"' + sub.url + '\", \"upvotes\": \"' + sub.ups + '\", \"redditId\": \"' + sub.id + '\", \"localFile\": \" \", \"captionText\": \" \", \"updateFlag\": \"false\", \"createdMemeFlag\": \"false\", \"upvoteTrend\": \"1\" }'
            insertPost = { 'url': sub.url,
              "upvotes": sub.ups,
              "redditId": sub.id,
              "localFile": " ",
              "captionText": " ",
              "updateFlag": "false",
              "createdMemeFlag": "false",
              "upvoteTrend": 1,
            }
            stringInsertPost = json.dumps(insertPost)
            stringInsertPost.replace('"',"'") # The json library does not allow for single quotes but requires double quotes
            # Upsert the document into the redditposts collection
            upvotepostsHandler.databaseMessage(msg=('[{\"redditId\": \"%s\"},{\"$set\": %s}]' % (sub.id, stringInsertPost)),operation="update") # Send a message to the database to update the stringInsertPost
            logHandler.logMessage('(newMemeIdentifier) Inserted document into redditposts with redditId %s' % sub.id)

            # Remove the document from the upvoteposts collection
            upvotepostsCollection.delete_one({'redditId':sub.id})
            logHandler.logMessage('(newMemeIdentifier) Removed document from upvoteposts with redditId %s' % sub.id)

        elif current['upvoteTrend'] < upvoteTrendNegativeCutoff:
            # If the upvoteTrend gets below -5 then delete the document and stop tracking it
            logHandler.logMessage('(newMemeIdentifier) Deleting document due to low upvoteTrend')

            # TODO: Change this to a rabbitmq message
            upvotepostsCollection.delete_one({"_id":current["_id"]})
        else:
            oldUpvotes = current['upvote'] # Upvotes of the saved state in the database
            newUpvotes = sub.ups     # Upvotes of the current post
            logHandler.logMessage('(newMemeIdentifier) Current Upvotes %s for id %s' % (newUpvotes,current['redditId']))

            # If the upvotes has increased by more than the exitvalue variable then increment the upvoteTrend
            if newUpvotes > oldUpvotes + exitvalue:
                logHandler.logMessage('(newMemeIdentifier) Updating Value for id %s' % current['redditId'])
                updatePost = {
                    'upvoteTrend': current['upvoteTrend'] + 1,
                    'upvote': newUpvotes,
                    }
                logHandler.logMessage('(newMemeIdentifier) Updating document with id %s' % current["_id"])
                # TODO: Change this update call to a rabbitmq message
                upvotepostsCollection.update_one({"_id": current["_id"]}, {"$set": updatePost})
            # If the upvotes has decremented by more than the exitvalue variable then decrement the upvoteTrend
            elif newUpvotes < oldUpvotes - exitvalue:
                logHandler.logMessage('(newMemeIdentifier) Downgrading Value for id %s' % current['redditId'])
                updatePost = {
                    'upvoteTrend': current['upvoteTrend'] - 1
                    }
                logHandler.logMessage('(newMemeIdentifier) Updating document with id %s' % current["_id"])
                # TODO Change this update call to a rabbitmq message
                upvotepostsCollection.update_one({"_id": current["_id"]}, {"$set": updatePost})

if __name__ == '__main__':
    logHandler.logMessage('(newMemeIdentifier) Starting main process')
    q = Queue.Queue()
    while not exitapp:
        logHandler.logMessage('(newMemeIdentifier) Starting checkDatabase')
        checkDatabase()
        timer = 300
        logHandler.logMessage('(newMemeIdentifier) Waiting for %i seconds' % timer)
        time.sleep(300)
