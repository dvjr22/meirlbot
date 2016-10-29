############################################################
#                    Google Downloader                     #
# Creator: Tyler Moon                                      #
# Contributors:                                            #
# Purpose: This script uses the most common keywords in    #
# the keywordsCondensed.txt file and scrapes Google Images #
# webpage. Once an image has been found it downloads it    #
# into the createdMemes directory                          #
############################################################
import urllib2
from bs4 import BeautifulSoup
import requests
import re
import os
import cookielib
import json
import logging
from logging.config import fileConfig
from pymongo import MongoClient

# Mongo database
client = MongoClient('mongodb://localhost:27017')
db = client['meirlbot_mongodb']
rposts = db.redditposts

# Configure the logger
fileConfig('../logging_config.ini')
logger = logging.getLogger()
handler = logging.handlers.RotatingFileHandler('../logs/memecreator.log')
logger.addHandler(handler)

def setup(query, current):
    def get_soup(url,header):
        print 'in get_soup'
        return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

    writeCounter = 0;
    def writeImage(ActualImages, index, current):
        print 'in writeImage'
        if index > 3:
            (img, Type) = ActualImages[index]
            try:
                req = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(req).read()

                cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
                print cntr
                path = ""
                if len(Type)==0:
                    path = str(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"))
                else:
                    path = os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type)

                f = open(path, 'wb')
                f.write(raw_img)
                f.close()
                print "Downloaded a meme"
                updatePost = {
                    'createdMemeFlag': True,
                    'createdMemeFile': path,
                }
                rposts.update_one({"_id": current["_id"]},{"$set": updatePost})
            except Exception as e:
                print "could not load : "+img
                print e
                writeImage(ActualImages, (index + 1),current)
        else:
            writeImage(ActualImages, (index + 1), current)


    #query = raw_input("query image")# you can change the query for the image  here
    image_type="meme"
    query= query.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    print url
    #add the directory for your image here
    DIR="createdMemes"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    soup = get_soup(url,header)


    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))

    print  "there are total" , len(ActualImages),"images"

    #if not os.path.exists(DIR):
    #            os.mkdir(DIR)
    #DIR = os.path.join(DIR, query.split()[0])

    #if not os.path.exists(DIR):
    #            os.mkdir(DIR)
    ###print images
    writeImage(ActualImages,0,current)


for current in rposts.find():
    if current['updateFlag']:
        print "downloading images for %s \n" % current['captionText']
        setup(current['captionText'],current)


#from icrawler.examples import GoogleImageCrawler

#kwd = "kittens"
#google_crawler = GoogleImageCrawler('createdMemes')
#google_crawler.crawl(keyword=kwd, offset=0, max_num=1,
#                     date_min=None, date_max=None, feeder_thr_num=1,
#                     parser_thr_num=1, downloader_thr_num=4,
#                     min_size=(200,200), max_size=None)
