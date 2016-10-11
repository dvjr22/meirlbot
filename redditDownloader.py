############################################################
# file:    redditDownloader.py                             #
# author:  Tyler Moon                                      #
# created: 10/11/2016                                      #
# purpose: This python program will download               #
#          the top images from a given reddit subreddit    #
############################################################
import re, praw, requests, os, glob, sys
from bs4 import BeautifulSoup

MIN_SCORE = 100 # Submittions below this score will not be downloaded

# sys.argv holds the command line arguments for python
if len(sys.argv) < 2:
    # There were no command line arguments set
    print('Usage: ')
    print('   python %s subreddit [minimum score]' % (sys.argv[0]))
    sys.exit()
elif len(sys.argv) >= 2:
    targetSubreddit = sys.argv[1] # The subreddit to download from
    if len(sys.argv) >= 3:
        # This means that the optional argument to change the MIN_SCORE has been set
        MIN_SCORE = int(sys.argv[2])

# Regex pattern for imgur links
imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')

# Function for downloading an image from a specified url to a specific local file location
def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
        with open(localFileName, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

# Connect to reddit and download the subreddit front page
r = praw.Reddit(user_agent='tmoonisthebest')
submissions = r.get_subreddit(targetSubreddit).get_hot(limit=25)

# Process all the submissions
for submission in submissions:
    # Check for all the cases where we would want to skip a submission
    if "imgur.com/" not in submission.url:
        # TODO: Will need to allow reddit image submissions at some point
        continue # skip non-imgur submissions
    if submission.score < MIN_SCORE:
        continue # Skip those low score memes nobody cares about
    if 'http://imgur.com/a/' in submission.url:
        # The /a denotes an album
        print('Downloading an album')
        albumId = submission.url[len('http://imgur.com/a/'):]
        htmlSource = requests.get(submission.url).text

        soup = BeautifulSoup(htmlSource)
        matches = soup.select('.album-view-image-link a')
        for match in matches:
            imageUrl = match['href']
            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1: imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]
            localFileName = 'reddit_%s_%s_album_%s_imgur_%s' % (targetSubreddit,submission.id, albumId, imageFile)
            downloadImage('http:' + match['href'], localFileName)

    elif 'http://i.imgur.com/' in submission.url:
        # The URL is a direct link to the imageFile
        print('Downloading a direct link')
        mo = imgurUrlPattern.search(submission.url)

        imgurFilename = mo.group(2)
        if '?' in imgurFilename:
            # The regex doesn't catch a "?" at the end of the filename so we remvoe it here
            imgurFilename = imgurFilename[:imgurFilename.find('?')]

        localFileName = 'reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imgurFilename)
        downloadImage(submission.url, localFileName)

    elif 'http://imgur.com/' in submission.url:
        # This is an Imgur page with a single image.
        print('Downloading a single image page')
        htmlSource = requests.get(submission.url).text # download the image's page
        soup = BeautifulSoup(htmlSource,"lxml")
        imageUrl = soup.select('link')[0]['href']
        if imageUrl.startswith('//'):
            # if no schema is supplied in the url, prepend 'http:' to it
            imageUrl = 'http:' + imageUrl
        imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

        if '?' in imageUrl:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
        else:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:]

        localFileName = 'reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imageFile)
        downloadImage(imageUrl, localFileName)
