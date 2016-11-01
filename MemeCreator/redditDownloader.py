############################################################
# file:    redditDownloader.py                             #
# author:  Tyler Moon                                      #
# created: 10/11/2016                                      #
# purpose: This python program will download               #
#          the top images from a given reddit subreddit    #
############################################################
import re, praw, requests, os, glob, sys, logging
from logging.config import fileConfig
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
rposts = db.redditposts

# Configure the logging
logging.basicConfig(filename='../logs/memecreator.log', level=logging.DEBUG)

MIN_SCORE = 100 # Submittions below this score will not be downloaded
LIMIT = 10000
targetSubreddit = "me_irl"
# Regex pattern for imgur links
imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')

# Function for downloading an image from a specified url to a specific local file location
def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        logging.info('Downloading %s...' % (localFileName))
        with open(localFileName, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

def parseImage(submission):
    logging.info('Parsing Image %s' % submission.id)
    # Check for all the cases where we would want to skip a submission
    #if "imgur.com/" not in submission.url:
    #if submission.score < MIN_SCORE:
    #        continue # Skip those low score memes nobody cares about
    if 'http://imgur.com/a/' in submission.url:
        # The /a denotes an album
        logging.debug('Downloading an album')
        albumId = submission.url[len('http://imgur.com/a/'):]
        htmlSource = requests.get(submission.url).text
        # Use BeautifulSoup to parse through the raw html code
        soup = BeautifulSoup(htmlSource)
        matches = soup.select('.album-view-image-link a')
        for match in matches:
            imageUrl = match['href']
            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1: imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]
            localFileName = './images/reddit_%s_%s_album_%s_imgur_%s' % (targetSubreddit,submission.id, albumId, imageFile)
            downloadImage('http:' + match['href'], localFileName)
            logging.debug('returning %s' % localFileName)
            return localFileName
    elif 'https://i.redd.it/' in submission.url:
        # This is a reddit upload page
        logging.debug('Downloading from i.redd.it %s' % submission.url)
        localFileName = './images/reddit_%s_%s_album_%s_reddit_%s' % (targetSubreddit,submission.id, "", ".jpg")
        downloadImage(submission.url, localFileName)
        logging.debug('returning %s' % localFileName)
        return localFileName
    elif 'https://i.reddituploads.com/' in submission.url:
        # This is a reddit upload page
        logging.debug('Downloading from i.reddituploads.com')
        localFileName = './images/reddit_%s_%s_album_%s_reddit_%s' % (targetSubreddit,submission.id, "", ".jpg")
        downloadImage(submission.url, localFileName)
        logging.debug('returning %s' % localFileName)
        return localFileName
    elif 'http://i.imgur.com/' in submission.url:
        # The URL is a direct link to the imageFile
        logging.debug('Downloading a direct link')
        mo = imgurUrlPattern.search(submission.url)

        imgurFilename = mo.group(2)
        if '?' in imgurFilename:
            # The regex doesn't catch a "?" at the end of the filename so we remvoe it here
            imgurFilename = imgurFilename[:imgurFilename.find('?')]

        localFileName = './images/reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imgurFilename)
        downloadImage(submission.url, localFileName)
        logging.debug('returning %s' % localFileName)
        return localFileName

    elif 'http://imgur.com/' in submission.url:
        # This is an Imgur page with a single image.
        logging.debug('Downloading a single image page')
        htmlSource = requests.get(submission.url).text # download the image's page
        soup = BeautifulSoup(htmlSource,"lxml")
        imageUrl = soup.select('img')[0]['src']
        if imageUrl.startswith('//'):
            # if no schema is supplied in the url, prepend 'http:' to it
            imageUrl = 'http:' + imageUrl
        imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]
        if '?' in imageUrl:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
        else:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:]

        localFileName = './images/reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imageFile)
        downloadImage(imageUrl, localFileName)
        logging.debug('returning %s' % localFileName)
        return localFileName


# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='tmoonisthebest')

logging.info('Reddit Downloader started')
# Process all the submissions
#for submission in submissions:
for current in rposts.find():
    logging.info("Searching through redditposts")
    submission = r.get_submission(submission_id=current['redditId'])
    oldUpvotes = current['upvotes'] # Upvotes of the saved state in the database
    newUpvotes = submission.ups     # Upvotes of the current post
    value = (float(newUpvotes) / oldUpvotes) * 100
    logging.debug("Reddit ID: %s Old Upvotes: %s New Upvotes: %s Difference %s Percent %s" % (submission.id, str(oldUpvotes), str(newUpvotes), str(abs(newUpvotes - oldUpvotes)), str(value)))
    # Only download the image if the change is sufficient
    if(value > 100.0):
        localFileName = parseImage(submission)
        # Add the local file path to the database and update the upvotes
        updatePost = {
                        'localFile': localFileName,
                        'upvotes': newUpvotes,
                        'url': submission.url,
                        'updateFlag': True,
                     }
        logging.debug("Inserting %s into redditposts document" % updatePost)
        rposts.update_one({"redditId": current['redditId']}, { "$set" : updatePost})
    else:
        logging.error ('Not Parsing Image %s due to too low of a change in upvotes' % submission.id)
logging.info('Reddit Downloader finished')
