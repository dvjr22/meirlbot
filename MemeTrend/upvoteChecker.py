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
databaseHandler = RabbitMQHandler(exchange='database', routing_key='upvotepostsupdate', queueType='direct')

# Boolean for passing the KeyboardInterrupt signal onto the threads
exitapp = False
# Simple function for returning a formatted datetime stamp
def getCurrentTime():
    return strftime("%Y-%m-%d %I:%m:%S")
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
            databaseHandler.publishMsg(json.dumps(updatePost))
            #upvotepostsCollection.update_one({'redditId': redditId}, {"$set": updatePost},True) # The true argument here inserts a new document if an exisiting one isnt found
        else:
            logHandler.publishMsg('(upvoteChecker) Submission %s already in database' % sub.id)
# Simple function that returns a boolean of if the document with the redditId newID already exists in the collection or not
def alreadyExists(newID):
    exists = bool(db.mycollection.find_one({'redditId': newID}))
    logHandler.publishMsg('(newMemeIdentifier) Already exists check for %s is %s' % (newID,exists))
    return exists
def main():
    logHandler.publishMsg('(upvoteChecker) Starting main process')
    q = Queue.Queue()
    while not exitapp:
        logHandler.publishMsg('(upvoteChecker) Starting loadFromReddit')
        loadFromReddit()
        timer = 300
        logHandler.publishMsg('(upvoteChecker) Waiting for %i seconds' % timer)
        time.sleep(timer)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        os.abort()
