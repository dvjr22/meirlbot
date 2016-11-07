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
from RabbitMQ.RabbitMQHandler import RabbitMQDatabase
from RabbitMQ.RabbitMQHandler import RabbitMQLogger
from RabbitMQ.RabbitMQHandler import RabbitMQFetch

# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='tmoonisthebest')

# Configure the RabbitMQ logger
logHandler = RabbitMQLogger()
databaseHandler = RabbitMQDatabase('upvoteposts')
fetchHandler = RabbitMQFetch()

# Boolean for passing the KeyboardInterrupt signal onto the threads
exitapp = False
# Simple function for returning a formatted datetime stamp
def getCurrentTime():
    return strftime("%Y-%m-%d %I:%m:%S")
# Simple function that returns a boolean of if the document with the redditId newID already exists in the collection or not
def alreadyExists(newID):
    query = {
      'redditId': newID
    }
    exists = fetchHandler.call(json.dumps(query))
    if(exists == '[]'):
        logHandler.logMessage('  [x] (upvoteChecker) redditId: %s does not already exists' % newID)
        return False
    logHandler.logMessage('  [x] (upvoteChecker) redditId: %s already exists' % newID)
    return True
# loadFromReddit is a function that loops through the top 100 posts on
# www.reddit.com/r/me_irl/new. As long as the submission is not already in the
# collection it adds to the collection upvoteposts
def loadFromReddit():
    submissions = r.get_subreddit("me_irl").get_new(limit=100)
    logHandler.logMessage('(upvoteChecker) Loading submissions %s' % submissions)
    logHandler.logMessage('(upvoteChecker) Loading in new data from reddit')
    for sub in submissions:
        if not alreadyExists(sub.id):
            upvoteTrend = 0
            redditId = sub.id
            url = sub.url
            upvotes = sub.ups
            logHandler.logMessage('(upvoteChecker) Inserting database document for %s, %s, %s, %s' % (upvotes, upvoteTrend, redditId, url))
            updatePost = {
                'upvoteTrend': upvoteTrend,
                'upvote': upvotes,
                'redditId': redditId,
                'url': url,
                'lastUpdate': getCurrentTime()
            }
            databaseHandler.databaseMessage(json.dumps(updatePost),'update')
        else:
            logHandler.logMessage('(upvoteChecker) Submission %s already in database' % sub.id)


# Start the script
if __name__ == '__main__':
    logHandler.logMessage('(upvoteChecker) Starting main process')
    # REVIEW: Perhaps not an inf loop
    while not exitapp:
        logHandler.logMessage('(upvoteChecker) Starting loadFromReddit')
        loadFromReddit()
        timer = 300
        logHandler.logMessage('(upvoteChecker) Waiting for %i seconds' % timer)
        time.sleep(timer)
