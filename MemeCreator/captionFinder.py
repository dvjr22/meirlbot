############################################################
#                      Caption Finder                      #
# Creator: Tyler Moon                                      #
# Contributors:                                            #
# Purpose: This script takes all the images where the      #
# updateFlag is true in the database, runs the images      #
# through the Google Image API to determine the captions   #
# of the images. These captions are then saved to the      #
# database                                                 #
############################################################
import argparse
import base64
import logging
import os
# Connection to the Google Vision API
from googleapiclient import discovery
# GoogleCredentials authentication library
from oauth2client.client import GoogleCredentials
# MongoDB Connection
from pymongo import MongoClient
# Logging config
from logging.config import fileConfig


# Global database objects
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
rposts = db.redditposts

# Configure the logger
fileConfig('../logging_config.ini')
logger = logging.getLogger()
handler = logging.handlers.RotatingFileHandler('../logs/memecreator.log')
logger.addHandler(handler)


def main(currentPost):
    # Load the credentials for the Google Vision API from the path variable $GOOGLE_APPLICATION_CREDENTIALS
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    # Get the path to the download image as specified in the database
    photo_file = currentPost['localFile']
    logger.debug('Searching for image %s' % photo_file)
    # Open the image file as passed in the parameter if it exists
    if (photo_file != None) and os.path.isfile(photo_file):
        with open(photo_file, 'rb') as image:
            # Encode the image to 64 bit
            image_content = base64.b64encode(image.read())
            # Parameters to pass to the Google Vision API
            service_request = service.images().annotate(body={
                'requests': [{
                    'image': {
                        # Image to load
                        'content': image_content.decode('UTF-8')
                    },
                    'features': [{
                        # Type of response
                        'type': 'TEXT_DETECTION',
                        # Number of results to return
                        'maxResults': 1
                    }]
                }]
            })
            # Get the json response from the API
            response = service_request.execute()
            logger.debug('Response from Google Vision API for image %s is %s' % (photo_file,response))
            # Parse the response from the API to pull out only the caption
            try:
                captionText = response['responses'][0]['textAnnotations'][0]['description'].replace('\n',' ')
                logger.debug('Parsed out %s as a caption for %s' % (captionText, photo_file))
                updatePost = {
                                'captionText': captionText,
                             }
                logger.debug('Updating database with %s' % updatePost)
                rposts.update_one({"_id": current['_id']}, { "$set" : updatePost})
            except KeyError as ke:
                logger.error('There was an error parsing the API response %s' % ke)

    else:
        logger.error('The file %s that is referenced in the database does not exist or cannot be opened' % photo_file)

if __name__ == '__main__':
    for current in rposts.find({"updateFlag": True}):
        logger.debug('Searching for captions in %s' % current)
        main(current)
